# Báo cáo Lab: Self evolving Agentic

Bản nháp theo [GUIDE](../GUIDE.md), [README](../README.md), [rubric](../RUBRIC.md) và [mẫu báo cáo](../REPORT_TEMPLATE.md). Nội dung kiến trúc xác nhận từ code; kết quả tests là kiểm tra offline trong phiên làm việc. Chưa có benchmark thật hoặc skill chính thức. `TODO: fill after real run` nghĩa là dữ liệu chưa thu thập, không phải giá trị 0. Chưa thực hiện API call, commit hoặc tag trong bước chuẩn bị báo cáo.

## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| TODO: xác nhận | TODO: xác nhận | TODO: xác nhận đóng góp |

- Model/deployment và `LAB_TEMPERATURE`: TODO: xác nhận cấu hình trước real run; không ghi khóa API.
- `recursion_limit`: mặc định CLI là 60; cấu hình thực nghiệm: TODO: fill after real run.
- Deep Agents: 0.7.21 trong pyproject và package đã kiểm tra trên Windows. Python dùng cho tests: 3.12.3.
- Môi trường tests: Windows, .venv, chạy trực tiếp. Linux/WSL/Docker cho thực nghiệm: TODO: xác nhận khi sẵn sàng.
- Số lần chạy tác vụ thật / ngân sách: TODO: fill after real run và xác nhận ngân sách với giảng viên; không tính tests fake model vào benchmark.
- Commit mã nguồn thực nghiệm: TODO: ghi trước chạy thật.
- Commit tag `freeze`: TODO: điền sau quy trình Phần 4.

### Kiến trúc tổng thể

[agent.py](../src/lab/agent.py) dùng `create_deep_agent()` để tạo graph. Main agent nhận đề bài qua messages, dùng công cụ tệp/shell, có thể delegate qua `task` và trả lời tổng kết. Deep Agents cung cấp vòng lặp model/tool và delegation; repo không yêu cầu Coordinator class riêng. Các provided constants BASE_PROMPT, PATHS_NOTE, SUBAGENTS_NOTE và SKILLS_NOTE được giữ nguyên.

| Condition | Mode | Subagents tự định nghĩa | Skill nguồn |
|---|---|---|---|
| baseline | single | Không thêm | Không có |
| subagents | subagents | explorer, implementer, reviewer | Không có |
| skills-auto | single | Không thêm | skills/auto/ |

Cả hai mode đều có general-purpose mặc định. Với subagents, build_agent nối PATHS_NOTE vào prompt từng agent và SUBAGENTS_NOTE vào prompt chính. Với skill, truyền đường dẫn ảo /skills/ và thêm SKILLS_NOTE. Custom subagents hiện không được cấu hình skills riêng.

### Runner, checks và metadata

Flow từ [runner.py](../src/lab/runner.py):

```text
condition/task → CONDITIONS/get_task → TemporaryDirectory/prepare_sandbox
→ hash skill trước → build_agent → invoke(messages, callbacks, recursion_limit)
→ metadata/hash sau/grade → trace.md → cleanup sandbox → run.json → trả record
```

Output: `<results_dir>/<condition>/<task_id>/run.json` và `trace.md`; results_dir mặc định là results.

| Trường record | Nguồn/ý nghĩa |
|---|---|
| task, condition, role | Task và cấu hình |
| timestamp | UTC ISO-8601 lúc bắt đầu record |
| seconds | Thời gian invoke bằng perf_counter, làm tròn 1 chữ số; không gồm setup/chấm điểm khi invoke chạy bình thường |
| tokens.input/output/total | UsageMetadataCallbackHandler cộng usage của mọi model call, kể cả subagents khi model cung cấp metadata |
| tool_calls, subagent_calls | Tool calls luồng chính; subagent_calls đếm tên task |
| skills_read | Số tên skill khác nhau trong read_file có đường dẫn chứa skills/; đọc không chứng minh làm theo |
| skills_sha256, skills_modified | Hash trước và so sánh hash skill sau chạy |
| score, passed, total, checks | grade() chạy checker trên workspace bản sao; check có name, passed, detail |
| final_message, error | Nội dung message cuối; lỗi build/invoke hoặc checker khi chưa có lỗi trước đó |

Helper grade giữ detail chỉ cho failed checks của learning; check đạt và mọi check evaluation có detail rỗng. render_trace có sẵn chỉ ghi luồng chính, thay đường dẫn home bằng ~ và giới hạn mỗi đoạn 1.500 ký tự. Token fake trong tests không đại diện chi phí API thật.

### Sandbox, đường dẫn và lỗi

Runner sao chép workspace gốc vào thư mục tạm hệ điều hành, cleanup bằng context manager. LocalShellBackend dùng root_dir=sandbox, virtual_mode=True, inherit_env=False; chỉ truyền PATH tối thiểu, HOME sandbox và PYTHONDONTWRITEBYTECODE=1. Timeout mỗi shell command là 120 giây. Agent dùng workspace/... và skills/... tương đối cho cả công cụ tệp và shell; /skills/ trong cấu hình là đường dẫn ảo. Virtual mode giới hạn đường dẫn công cụ tệp, không cô lập quyền truy cập của shell trên hệ điều hành.

Lỗi build/invoke lưu dạng ExceptionType: message; vẫn chấm workspace và ghi record. Khi invoke lỗi, messages/final rỗng, trace rỗng và tool counts bằng 0 dù có thể đã thực hiện bước trước đó; callback giữ usage đã thu. Lỗi chuẩn bị sandbox/ghi file chưa có record thay thế; CLI có sẵn báo CRASH. Không dùng lỗi hạ tầng làm evidence phân loại lỗi agent.

## 2. Giả thuyết (commit TRƯỚC tag freeze, Phần 4.0)

Phải viết dự đoán có căn cứ từ learning và tài liệu TRƯỚC khi thấy điểm evaluation, rồi có commit hypotheses trước tag freeze. Chưa thực hiện quy trình này.

- H1 (subagents so với baseline):
- H2 (skills-auto so với baseline):
- H3 (tác vụ học so với tác vụ đánh giá):

TODO: điền H1–H3 sau phân tích learning, trước evaluation. Giữ giá trị sau dấu hai chấm trống trong skeleton để verify_freeze.py không nhận nhầm placeholder thành giả thuyết đã điền.

## 3. Làm quen Deep Agents (Phần 0.3)

1. Theo GUIDE và scripts/tour.py: ls, read_file, write_file, edit_file, delete, glob, grep, execute, task. execute chạy shell; task delegate. TODO: đối chiếu và lưu output thực tế của python scripts/tour.py.
2. Guide subagents mô tả ngữ cảnh riêng, chỉ nhận lời giao việc và trả báo cáo cuối; main agent cần truyền đủ quy tắc/đường dẫn. general-purpose là subagent mặc định. TODO: trích mô tả runtime của task về ngữ cảnh general-purpose từ tour.
3. Main agent lab có BASE_PROMPT; tour khảo sát agent mặc định không truyền prompt này. TODO: lấy đúng một câu hướng dẫn từ mô tả runtime task và một câu từ execute, kèm output nguồn. Chưa có trích dẫn runtime được thu thập.

## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)

Chỉ dùng learning real runs. Nhóm A–G theo GUIDE: bỏ qua đặc tả; không kiểm chứng; vá triệu chứng; bỏ sót dữ liệu bẩn/định dạng; vi phạm quy ước; báo cáo hoàn thành sai; khác.

| Tác vụ | Failed check | Nhóm A–G | Bằng chứng detail/trace và đường dẫn nguồn |
|---|---|---|---|
| TODO: fill after real run | TODO: fill after real run | TODO: fill after real run | TODO: fill after real run |

TODO: phân loại ít nhất 4 failed checks nếu dữ liệu thật có đủ theo rubric; không bịa lỗi để đủ dòng. Nêu nhóm đa số, nguyên nhân chung, khả năng phòng ngừa bằng skill. Nếu lỗi chỉ thuộc một nhóm, thêm evidence phủ định cho nhóm khác bằng technical checks đạt/tổng từ check_breakdown.py.

Score, số task thành công/thất bại, latency, tokens và tool calls baseline: TODO: fill after real run từ results/baseline/<learning-task>/run.json và trace.md.

## 5. Điều kiện subagents (Phần 2.3)

Thiết kế từ [subagents.py](../src/lab/subagents.py):

| Agent | Khi gọi/vai trò | Ranh giới và báo cáo |
|---|---|---|
| explorer | Trước thay đổi, khảo sát tài liệu/code/dữ liệu và nguyên nhân | Không sửa file; báo bằng chứng, ràng buộc, điểm chưa rõ |
| implementer | Task/tiêu chí nghiệm thu đã rõ, cần sửa code/xử lý dữ liệu | Thực hiện trong scope, chạy checks; báo file thực sự thay đổi và kết quả quan sát |
| reviewer | Sau triển khai, kiểm tra độc lập trước kết luận hoàn thành | Không sửa file; kiểm tra output/edge cases; báo findings và điều chưa kiểm chứng |

Main agent thấy tên/descriptions qua task, tự chọn agent để delegate. Phân công nhằm tách khảo sát, thực hiện và kiểm tra độc lập; đây là ý định thiết kế, chưa phải hiệu quả đã đo.

- subagent_calls từng task, tên agent và số lần gọi: TODO: fill after real run.
- Lời giao việc có đủ quy tắc/đường dẫn, main kiểm tra báo cáo thế nào: TODO: fill after real run, dẫn đoạn trace.md.
- Score/token usage/tool calls/latency so baseline: TODO: fill after real run.
- Nếu subagent_calls bằng 0, báo đúng record và giải thích từ vết; đó là kết quả hợp lệ theo GUIDE.

## 6. Self-evolving: skill do curator sinh (Phần 3)

[curator.py](../src/lab/curator.py) đọc run.json theo thứ tự ổn định, chỉ lấy role=learn, thu failed check name/detail và tối đa 6.000 ký tự cuối trace. Không có failed checks hoặc max_skills <= 0 thì không gọi model. Có feedback thì gọi model được inject một lần bằng prompt yêu cầu quy trình tổng quát.

Reply dùng khối === SKILL: <name> === và === END ===. parse_skill_blocks có sẵn xử lý cả thiếu END. Curator validate trước ghi, loại skill lỗi/trùng tên, ghi tối đa max_skills (mặc định 3) vào skills/auto/<name>/SKILL.md và trả danh sách Path.

Schema: YAML frontmatter name/description rồi body Markdown. Validator yêu cầu tên an toàn tối đa 64 ký tự/trùng tên khối, description có và tối đa 1.024 ký tự, body tối đa 80 dòng, không chứa evaluation markers. Prompt khuyến nghị tối đa 40 dòng body. Validator không chứng minh nội dung đúng/hữu ích.

Chưa có skill chính thức từ learning baseline thật. Số lần curator thật, skill sinh/xóa và lý do chạy lại: TODO: fill after real run. Không sửa tay skill; chỉ xóa/chạy lại trong giới hạn GUIDE và ghi lý do.

| Skill/file nguồn | Tổng quát hay riêng learning? | Đúng/sai và feedback | Số dòng, description, skills_read Part 3.4 |
|---|---|---|---|
| TODO: fill after real run | TODO: fill after real run | TODO: fill after real run | TODO: fill after real run |

TODO: đối chiếu skills_read với từng quy tắc trong trace; đọc skill không đồng nghĩa làm theo. Sao lưu kết quả Part 3.4 thành results/skills-auto-dev trước khi chạy chính thức.

## 7. Kết quả so sánh (Phần 4.3, 4.4)

TODO: fill after real run. Sinh report/table.md bằng python -m lab.compare > report/table.md sau khi đủ records chính thức, rồi dán bảng ở đây. Không dựng số liệu bằng tay; chưa tạo table.md vì chưa có records thật.

```text
TODO: fill after real run — bảng 3 conditions, 6 tasks và hàng tổng hợp.
TODO: fill after real run — output python scripts/check_breakdown.py.
```

TODO: liệt kê run có error/skills_modified=true, đường dẫn, cách xử lý và lần chạy lại. Tách learning/evaluation và technical/house-rule checks. verify_freeze.py đã báo thiếu tag freeze trong kiểm tra trước; checkpoint Part 4 chưa đạt. Output OK chính thức: TODO: điền sau freeze và real runs.

## 8. Phân tích

1. Condition cải thiện learning/evaluation, cải thiện chỉ learning và overfitting: TODO: fill after real run.
2. Technical so rule_ checks, gồm rule mới evaluation: TODO: fill after real run từ breakdown/vết.
3. Một check skill giúp và một check không giúp; cơ chế đọc/làm theo/thiếu/sai: TODO: fill after real run, dẫn skills_read, SKILL.md và trace.
4. Token trung bình, score/token và chi phí subagents: TODO: fill after real run; ghi công thức và tập records.
5. Leakage/overfitting quan sát: TODO: fill after real run. Code có lọc role=learn và validate markers; quy trình còn phải hoàn thành: hypotheses trước freeze, không xem điểm eval trước đó, không sửa skill sau freeze.
6. Nhiễu cùng bộ skill ở Part 3.4 so sau freeze: TODO: fill after real run từ skills-auto-dev và skills-auto.

## 9. Hạn chế và tính hợp lệ

1. Windows thiếu which/cat trong cmd; README yêu cầu Linux/macOS hoặc WSL/Docker. Chưa xác nhận checkpoint agent 9/9 trên môi trường yêu cầu.
2. Thiết kế chỉ có 3 learning/3 evaluation tasks; không đại diện mọi tác vụ thực tế.
3. Một lần chạy mỗi cấu hình theo quy trình chính không đủ đánh giá biến thiên chắc chắn; cần đối chiếu cùng skill trước/sau freeze, nếu mở rộng thì lặp ở thư mục riêng.
4. Trace chỉ gồm luồng chính, cắt từng đoạn; không thấy toàn bộ công việc subagents. Invoke lỗi mất messages nên tool counts không phản ánh hết hoạt động trước lỗi.
5. Skill hợp lệ vẫn có thể sai/quá khớp; phải đánh giá feedback/nội dung/evaluation. Chưa có dữ liệu thật để kết luận hiệu quả.
6. Hash/timestamp hỗ trợ kiểm tra quy trình, không thay thế giữ dữ liệu evaluation ngoài việc học/viết giả thuyết.

## 10. Kết luận

Đã implement backend, agent, runner và curator theo skeleton và kiểm tra chức năng offline. Checkpoint agent trên Linux và thực nghiệm thật còn chờ. TODO: fill after real run — kết luận cuối tối đa 5 câu, chỉ khẳng định có số liệu hỗ trợ và một đề xuất tiếp theo.

## Phụ lục

### Tests offline đã thực hiện

Đây là tests code, không phải số task benchmark pass/fail. Output đã quan sát trong phiên làm việc; TODO: lưu output tái lập trước nộp.

| Lệnh (Python .venv) | Kết quả quan sát |
|---|---|
| python -m pytest tests/test_02_agent.py::test_subagents_have_required_fields -v | 1 PASS |
| python -m pytest tests/test_02_agent.py -v | 7 PASS, 2 FAIL do shell Windows |
| python -m pytest tests/test_03_runner.py -v | 6 PASS |
| python -m pytest tests/test_02_agent.py tests/test_03_runner.py -v | 13 PASS, 2 FAIL do shell Windows |
| python -m pytest tests/test_04_curator.py -v | 2 PASS |
| python -m pytest tests/ -q -k 'not backend_finds_python_and_hides_secrets and not file_tools_and_shell_share_relative_paths' | 27 PASS, loại 2 tests shell |
| python scripts/verify_freeze.py | FAIL: thiếu tag freeze |

Hai tests shell là test_backend_finds_python_and_hides_secrets và test_file_tools_and_shell_share_relative_paths. Full suite Linux: TODO: chạy/lưu output; không coi bộ đã loại tests là full-suite PASS.

### Checklist evidence theo phase

Ô hoàn thành ghi nhận code/tests đã quan sát; ô trống là evidence chưa đủ. Lệnh API thật dưới đây là kế hoạch theo GUIDE, chưa chạy.

#### Part 0 — Cài đặt/làm quen

- [x] Có .venv và Deep Agents 0.7.21 đã kiểm tra trên Windows.
- [ ] Linux/WSL/Docker sẵn sàng; ghi OS, Python/package versions, model configuration không chứa secret.
- [ ] Lưu output python -m pytest tests/test_01_provided.py: kỳ vọng 12 PASS; bộ này đã nằm trong 27 PASS nhưng cần evidence riêng.
- [ ] Lưu output python scripts/tour.py, điền mục 3 với hai trích dẫn runtime.
- [ ] Kiểm tra kết nối model theo GUIDE 0.2 khi được yêu cầu, lưu output không có secret.

#### Part 1 — Harness

- [x] Implement get_subagents, make_backend, build_agent, run_task; cấu trúc subagents PASS, runner 6/6 PASS fake model.
- [ ] Lưu tests/test_02_agent.py trên Linux: 9/9 PASS, và runner trên môi trường thực nghiệm.
- [ ] Khi được yêu cầu, chạy python -m lab.runner --condition baseline --tasks data-learn.
- [ ] Có results/baseline/data-learn/run.json và trace.md; tokens.total > 0, checks/detail đúng schema, kiểm tra error. Tính run này vào baseline learning, không chạy lại vô ích ở Part 2.

#### Part 2 — Learning/phân loại lỗi

- [ ] Chạy baseline code-learn logs-learn và subagents learn; lưu lệnh/cấu hình/output console.
- [ ] Có run.json và trace.md ở results/{baseline,subagents}/{code-learn,data-learn,logs-learn}/ (6 cặp learning).
- [ ] Mục 4 có check, nhóm A–G, trích detail/trace, file nguồn; loại lỗi hạ tầng và thêm evidence phủ định theo rubric.
- [ ] Mục 5 có subagent_calls, tên agent trong task calls, chất lượng lời giao việc/kiểm tra báo cáo và so sánh tokens/seconds.

#### Part 3 — Curator/skill

- [x] Implement curate_skills; 2 tests curator và validator/parser tests PASS offline.
- [ ] Lưu output curator tests riêng để tái lập.
- [ ] Có baseline learning thật trước python -m lab.curator; lưu output, lý do xóa/chạy lại.
- [ ] Ít nhất một skills/auto/<name>/SKILL.md do curator sinh, validate_skill trả [], không sửa tay.
- [ ] Mục 6 đánh giá từng skill theo guide 05: tổng quát, đúng/sai, độ dài/description.
- [ ] Có results/skills-auto/{code-learn,data-learn,logs-learn}/run.json và trace.md từ Part 3.4; đối chiếu skills_read với hành vi.
- [ ] Sao lưu Part 3.4 thành results/skills-auto-dev/ trước chạy frozen skills.

#### Part 4 — Hypotheses/freeze/evaluation

- [ ] H1–H3 có dự đoán/căn cứ trước điểm eval; commit hypotheses trước tag freeze (chưa thực hiện commit trong phiên này).
- [ ] Chốt skill, commit/tag theo GUIDE; ghi commit/hash, không đổi skills sau freeze.
- [ ] Chạy baseline/subagents eval, skills-auto all sau freeze; lưu lệnh/cấu hình/output.
- [ ] Mỗi condition baseline/subagents/skills-auto có run.json và trace.md cho cả 6 tasks (18 cặp chính thức); loại backups khỏi bảng chính.
- [ ] skills_sha256 khớp frozen skills, timestamp sau freeze, skills_modified=false; ghi và xử lý mọi run lỗi.
- [ ] Lưu python scripts/verify_freeze.py: OK; kiểm tra đủ 6 skills-auto records, không chỉ tag tồn tại.
- [ ] Sinh report/table.md bằng lab.compare: đủ 3 conditions/6 task rows/hàng tổng hợp, khớp records.
- [ ] Lưu check_breakdown.py output, dán cùng bảng vào mục 7.

#### Final report — Part 5/nộp bài

- [ ] Đủ mục 1–10, thay mọi placeholder bằng evidence hoặc ghi rõ chưa hoàn thành.
- [ ] Đối chiếu số liệu với run.json; tách offline tests/benchmark, learning/eval, technical/rule checks.
- [ ] Phân tích token cost, delegation/skill usage, leakage/overfitting và nhiễu cùng skill trước/sau freeze.
- [ ] Ít nhất 3 hạn chế kèm ảnh hưởng; kết luận tối đa 5 câu dựa evidence.
- [ ] Lưu full-suite Linux, verify_freeze OK, versions/config/lệnh theo thứ tự/commit để tái lập.
- [ ] Có REPORT.md, table.md, skills chính thức và results liên quan; không có secret.
- [ ] Part 6 nếu làm: chọn hướng, results thư mục riêng, số liệu và phân tích phụ lục; hiện chưa thực hiện.

### Nhật ký và tài liệu

- Real-run commands theo thứ tự, cấu hình, chạy lại/lý do: TODO: fill after real run.
- Căn cứ H1–H3: TODO: ghi tài liệu đã đọc trước evaluation; không coi số liệu tham khảo trong pseudocode là số liệu của nhóm.
- Thử thách mở rộng: chưa thực hiện; TODO: ghi quyết định sau phần chính.
- Guides: [agent](../guides/pseudocode/01_agent.md), [subagents](../guides/pseudocode/02_subagents.md), [runner](../guides/pseudocode/03_runner.md), [curator](../guides/pseudocode/04_curator.md), [skill quality](../guides/pseudocode/05_skill_quality.md).
