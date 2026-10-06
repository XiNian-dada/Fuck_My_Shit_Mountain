"""Regression cases for observable report validation behavior."""
import contextlib
import html
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'fuck-my-shit-mountain/scripts'))
import report_lint as lint
from schema_validation import validate_schema


def finding():
    return dict(id='F1', title='Missing owner check', severity='High', confidence='High',
                category='security', status='Confirmed', affectedArea='account API',
                evidence={'file':'src/auth.py:12', 'functionOrModule':'get_account', 'relevantBehavior':'The route returns records without an owner check.'},
                problem='The account route omits authorization.', userVisibleImpact='Another user can read the account.',
                failureScenario='Request an account belonging to another authenticated user.',
                minimalFix='Check ownership before reading.', regressionTestSuggestion='Assert a forbidden response for another owner.',
                estimatedEffort='1 hour')


def stats(findings):
    result = []
    for severity in lint.SEVERITIES:
        rows = [f for f in findings if f['severity'] == severity]
        result.append(dict(severity=severity, count=len(rows), confirmed=sum(f['status']=='Confirmed' for f in rows), suspected=sum(f['status']=='Suspected' for f in rows)))
    return result


def json_report(findings=None):
    findings = [] if findings is None else findings
    return {
        'metadata': {'project':'fixture', 'auditModes':['security'], 'date':'2026-10-07', 'reviewer':'fixture', 'commitHash':None},
        'executiveSummary': {'text':'已检查权限边界。'},
        'scoreDashboard': {'dimensions':[{'name':'Security', 'score':7.0, 'grade':'A', 'justification':'Inspected account boundaries.', 'coverageConfidence':'High'}], 'overall':{'score':7.0,'grade':'A'}},
        'findingStatistics': {'bySeverity':stats(findings), 'total':{'count':len(findings),'confirmed':sum(f['status']=='Confirmed' for f in findings),'suspected':sum(f['status']=='Suspected' for f in findings)}},
        'projectMap': {'structure':'src', 'keyComponents':['API'], 'riskAreas':['auth']},
        'coverageMatrix': [{'dimension':'security','coverage':'High','evidenceInspected':'src/auth.py','exclusions':'No runtime check'}],
        'topRisks':[], 'detailedFindings':findings, 'dimensionSections':{'security':{'summary':'Checked account access.'}},
        'fixOrder':[], 'quickWins':[]
    }


def markdown_report(findings=None, translated=False):
    findings = [] if findings is None else findings
    text = '\n'.join(f'<!-- section:{section} -->\n## {labels[-1] if translated else labels[0]}' for section, labels in lint.SECTIONS.items())
    text += '\n<!-- section:security -->\n## 安全分析\n'
    text += '\n| Severity | Count | Confirmed | Suspected |\n|---|---|---|---|\n'
    for row in stats(findings):
        text += f"| {row['severity']} | {row['count']} | {row['confirmed']} | {row['suspected']} |\n"
    text += f"| Total | {len(findings)} | {sum(f['status']=='Confirmed' for f in findings)} | {sum(f['status']=='Suspected' for f in findings)} |\n"
    for item in findings:
        text += f"\n<!-- finding:{item['id']} -->\n### 发现：权限缺失\n"
        for field, labels in lint.FIELDS.items():
            value = item[field]
            if isinstance(value, dict):
                value = '\n  - ' + '\n  - '.join(f'{k}: {v}' for k, v in value.items())
            text += f"- {labels[-1] if translated else labels[0]}: <!-- field:{field} --> {value}\n"
    return text


def html_report(findings=None):
    findings = [] if findings is None else findings
    text = '<!DOCTYPE html><html><body>'
    text += ''.join(f'<section id="{key}">中文标题</section>' for key in (*lint.SECTIONS, 'security'))
    for row in [*stats(findings), {'severity':'Total', 'count':len(findings), 'confirmed':sum(f['status']=='Confirmed' for f in findings), 'suspected':sum(f['status']=='Suspected' for f in findings)}]:
        text += f"<div data-stat=\"{row['severity']}\" data-count=\"{row['count']}\" data-confirmed=\"{row['confirmed']}\" data-suspected=\"{row['suspected']}\">统计</div>"
    for item in findings:
        text += f'<article data-finding="{item["id"]}">'
        for field in lint.FIELDS:
            text += f'<div data-field="{field}">{item[field]}</div>'
        text += '</article>'
    return text + '</body></html>'


class ReportLintTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)

    def check(self, content, suffix, modes='security'):
        path = Path(self.temp.name) / ('report' + suffix)
        path.write_text(json.dumps(content, ensure_ascii=False) if isinstance(content, dict) else content, encoding='utf-8')
        return lint.lint_report(path, modes)

    def test_all_formats_accept_zero_and_confirmed_findings(self):
        for findings in ([], [finding()]):
            for builder, suffix in ((json_report, '.json'), (markdown_report, '.md'), (html_report, '.html')):
                with self.subTest(suffix=suffix, findings=len(findings)):
                    self.assertEqual(self.check(builder(findings), suffix), [])

    def test_localized_markdown_and_stable_markers(self):
        self.assertEqual(self.check(markdown_report([finding()], translated=True), '.md'), [])
        text = markdown_report([finding()], translated=True)
        for labels in lint.SECTIONS.values():
            text = text.replace(labels[-1], 'Résumé')
        for labels in lint.FIELDS.values():
            text = text.replace(labels[-1] + ':', 'Champ:')
        self.assertEqual(self.check(text, '.md'), [])

    def test_modes_include_concurrency_and_incremental(self):
        for modes in ('full', 'incremental'):
            issues = []
            self.assertIn('concurrency', lint.expand_modes(modes, issues))
            self.assertEqual(issues, [])
        self.assertEqual(lint.expand_modes('incremental,security', []), ('security',))
        issues = []
        lint.expand_modes('made-up', issues)
        self.assertTrue(issues)

    def test_missing_concurrency_is_detected_in_full_audit(self):
        text = markdown_report() + '\n'.join(f'<!-- section:{mode} -->' for mode in lint.FULL_SECTION_IDS if mode != 'concurrency')
        self.assertIn('Missing selected dimension section: concurrency', self.check(text, '.md', 'full'))

    def test_secret_diagnostics_never_echo_matched_values(self):
        secret = 'synthetic_test_value_1234'
        for text in ('api_key=' + secret, '"api_key": "' + secret + '"', 'password=&quot;' + secret + '&quot;'):
            issues = []
            lint.lint_secrets(text, issues)
            self.assertTrue(issues)
            self.assertNotIn(secret, ' '.join(issues))
        for value in ('<redacted>', '&lt;redacted&gt;'):
            issues = []
            lint.lint_secrets('api_key=' + value, issues)
            self.assertEqual(issues, [])

    def test_json_decoded_secret_is_checked(self):
        content = json.dumps(json_report(), ensure_ascii=False).replace('已检查权限边界。', 'api_key=synthetic_test_value_1234')
        content = content.replace('api_key', 'api\\u005fkey')
        self.assertTrue(any('secret' in error for error in self.check(content, '.json')))

    def test_missing_empty_or_invalid_finding_fields_fail(self):
        for suffix, builder in (('.json', json_report), ('.md', markdown_report), ('.html', html_report)):
            broken = finding()
            broken['minimalFix'] = ''
            broken['severity'] = 'Severe'
            self.assertTrue(self.check(builder([broken]), suffix))

    def test_optional_long_term_fix_is_not_required(self):
        self.assertEqual(self.check(json_report([finding()]), '.json'), [])

    def test_stats_must_match_status_and_severity(self):
        report = json_report([finding()])
        report['findingStatistics']['bySeverity'][1]['confirmed'] = 0
        self.assertTrue(any('statistics' in issue for issue in self.check(report, '.json')))
        for suffix, content in (('.md', markdown_report([finding()]).replace('| High | 1 | 1 | 0 |', '| High | 0 | 0 | 0 |')),
                                ('.html', html_report([finding()]).replace('data-count="1"', 'data-count="0"'))):
            self.assertTrue(any('statistics' in issue for issue in self.check(content, suffix)))

    def test_json_invalid_types_dates_and_structure_fail(self):
        for mutate in (lambda r: r.pop('metadata'), lambda r: r['metadata'].update(date='2026-02-30'),
                       lambda r: r['scoreDashboard']['dimensions'][0].update(score=True),
                       lambda r: r['scoreDashboard']['dimensions'][0].update(score=11),
                       lambda r: r['dimensionSections'].clear()):
            report = json_report()
            mutate(report)
            self.assertTrue(self.check(report, '.json'))
        for content in ('[]', '{', '{"a":1,"a":2}', '{"a":NaN}'):
            self.assertTrue(self.check(content, '.json'))

    def test_duplicate_ids_and_dangling_references_fail(self):
        report = json_report([finding(), finding()])
        self.assertTrue(any('Duplicate finding' in issue for issue in self.check(report, '.json')))
        report = json_report([finding()])
        report['quickWins'] = [{'findingId':'absent','effort':'1 hour','impact':'Less risk'}]
        self.assertTrue(any('reference' in issue for issue in self.check(report, '.json')))

    def test_not_assessed_scores_are_excluded(self):
        report = json_report()
        report['scoreDashboard']['dimensions'].append({'name':'Testing','score':None,'grade':None,'justification':'Outside scope','coverageConfidence':'Not assessed'})
        self.assertEqual(self.check(report, '.json'), [])
        report['scoreDashboard']['dimensions'][0].update(score=None, grade=None, coverageConfidence='Not assessed')
        report['scoreDashboard']['overall'].update(score=None, grade=None)
        self.assertEqual(self.check(report, '.json'), [])

    def test_overall_weights_and_grade_are_consistent(self):
        report = json_report()
        report['scoreDashboard']['dimensions'].append({'name':'Testing','score':5,'grade':'B','justification':'Critical behavior inspected','coverageConfidence':'High'})
        report['scoreDashboard']['intelligentWeights'] = {'weights':{'Security':0.75,'Testing':0.25},'reasoning':'Requested focus'}
        report['scoreDashboard']['overall'].update(score=6.5, grade='B')
        self.assertEqual(self.check(report, '.json'), [])
        report['scoreDashboard']['overall']['score'] = 6
        self.assertTrue(any('Overall' in issue for issue in self.check(report, '.json')))

    def test_incremental_json_requires_resolved_scope(self):
        report = json_report()
        report['metadata']['auditModes'] = ['incremental', 'security']
        self.assertTrue(self.check(report, '.json', 'incremental,security'))
        report['metadata']['scope'] = 'main...HEAD; merge base abc123, head def456'
        self.assertEqual(self.check(report, '.json', 'incremental,security'), [])

    def test_html_comment_cannot_fake_a_section(self):
        text = html_report().replace('<section id="security">中文标题</section>', '<!-- id="security" -->')
        self.assertIn('Missing HTML section id: security', self.check(text, '.html'))

    def test_html_broken_links_and_malformed_tags_fail(self):
        self.assertTrue(self.check(html_report().replace('</body>', '<a href="#absent">Link</a></body>'), '.html'))
        self.assertTrue(self.check(html_report().replace('</body>', '<div></body>'), '.html'))

    def test_findings_inside_code_fences_do_not_change_stats(self):
        text = markdown_report() + '\n```\n### Finding: Example\n- Severity: High\n```\n'
        self.assertEqual(self.check(text, '.md'), [])

    def test_cli_keeps_unreadable_file_exit_code(self):
        path = Path(self.temp.name) / 'bad.json'
        path.write_text('{}')
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(lint.main([str(path.with_name('missing.json')), str(path)]), 2)

    def test_schema_changes_cannot_silently_skip_constraints(self):
        self.assertTrue(validate_schema('abc', {'type':'string', 'pattern':'^x'}))

    def test_real_templates_produce_consistent_reports(self):
        import re
        skill = ROOT / 'fuck-my-shit-mountain'
        for has_finding in (False, True):
            item = finding()
            counts = stats([item] if has_finding else [])
            values = dict(PROJECT='示例项目', LANGUAGE_TAG='zh-CN', DIMENSION_ID='security',
                          FINDING_ID='F1', TITLE=item['title'], FINDING_TITLE=item['title'],
                          SEVERITY='High', SEVERITY_CLASS='high', STATUS='Confirmed',
                          CONFIDENCE='High', CATEGORY='security', AFFECTED_AREA=item['affectedArea'],
                          FILE_AND_LOCATION=item['evidence']['file'], FUNCTION_OR_MODULE='get_account',
                          RELEVANT_BEHAVIOR=item['evidence']['relevantBehavior'], PROBLEM=item['problem'],
                          IMPACT=item['userVisibleImpact'], FAILURE_SCENARIO=item['failureScenario'],
                          MINIMAL_FIX=item['minimalFix'], REGRESSION_VERIFICATION=item['regressionTestSuggestion'],
                          ESTIMATED_EFFORT=item['estimatedEffort'], SCORE_PERCENT='70', GRADE_CLASS='a',
                          DIMENSION_NAV_LINKS='<a href="#security">安全分析</a>',
                          ESCAPED_FILE_LOCATION_FUNCTION_AND_BEHAVIOR=html.escape(item['evidence']['file'] + ' ' + item['evidence']['relevantBehavior']))
            for row in [*counts, {'severity':'Total', 'count':int(has_finding), 'confirmed':int(has_finding), 'suspected':0}]:
                for column in ('count', 'confirmed', 'suspected'):
                    values[row['severity'].upper() + '_' + column.upper()] = str(row[column])
            def fill(text):
                return re.sub(r'\[\[([^\]]+)\]\]', lambda m: values.get(m.group(1), '检查说明'), text)
            card = fill((skill / 'templates/issue-card.md').read_text()) if has_finding else '检查范围内未发现达到报告阈值的问题。'
            values['FINDING_CARDS_OR_NO_FINDINGS_EXPLANATION'] = card
            md = fill((skill / 'templates/audit-report.md').read_text())
            page = (skill / 'templates/audit-report.html').read_text()
            if not has_finding:
                page = re.sub(r'<article\b.*?</article>', '<p>检查范围内未发现问题。</p>', page, flags=re.S)
            self.assertEqual(self.check(md, '.md'), [])
            self.assertEqual(self.check(fill(page), '.html'), [])

    def test_schema_mode_enum_matches_available_prompts(self):
        schema = json.loads((ROOT / 'fuck-my-shit-mountain/templates/audit-report.json').read_text())
        modes = schema['properties']['metadata']['properties']['auditModes']['items']['enum']
        self.assertEqual(set(modes), {'full', 'incremental', *lint.FULL_SECTION_IDS})


if __name__ == '__main__':
    unittest.main()
