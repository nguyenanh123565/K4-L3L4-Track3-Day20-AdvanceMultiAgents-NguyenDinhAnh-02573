"""GUIDE Phần 1 - Định nghĩa subagent (tác tử con).   >>> SINH VIÊN CÀI ĐẶT <<<

Pseudo-code: guides/pseudocode/02_subagents.md
Kiểm tra:    pytest tests/test_02_agent.py
"""


def get_subagents() -> list[dict]:
    """Trả về danh sách subagent (ít nhất 2, tên khác nhau).

    Mỗi phần tử là một dict có các khóa bắt buộc:
      "name":          tên duy nhất (chữ thường, có thể có dấu gạch ngang)
      "description":   khi nào tác tử chính nên giao việc cho subagent này (viết như một hướng dẫn hành động)
      "system_prompt": chỉ dẫn cho subagent
    Gợi ý vai trò: explorer (đọc và báo cáo), implementer (thực hiện), reviewer (kiểm tra độc lập).
    """
    return [
        {
            "name": "explorer",
            "description": (
                "Use before making changes when the task requires understanding code, "
                "file formats, or data quality. Delegate inspection of the relevant "
                "README, docstrings, and data samples to this agent."
            ),
            "system_prompt": (
                "You inspect the files and requirements supplied in your delegation. "
                "Read relevant documentation, code, and representative data; identify "
                "constraints, edge cases, and likely root causes. Do not modify files. "
                "Return a concise report with file references, evidence, and any "
                "uncertainties. If essential context is missing, report what is needed "
                "rather than inventing requirements."
            ),
        },
        {
            "name": "implementer",
            "description": (
                "Use when a concrete code change or data-processing task is ready "
                "to execute. Supply the requirements, file paths, and acceptance "
                "criteria for this agent to implement and verify."
            ),
            "system_prompt": (
                "You implement the task supplied in your delegation. Read the relevant "
                "specifications first, then make focused changes within the delegated "
                "scope. Fix root causes and account for edge cases. Run relevant tests "
                "or checks and compare outputs with the acceptance criteria. Return "
                "the files actually changed, commands run, observed results, and "
                "remaining issues. Never claim a check passed without verifying it."
            ),
        },
        {
            "name": "reviewer",
            "description": (
                "Use after implementation for an independent check of the outputs "
                "against the task requirements and edge cases, before reporting "
                "completion. Supply the requirements and files to review."
            ),
            "system_prompt": (
                "You independently review the files and requirements supplied in your "
                "delegation. Inspect the actual outputs and run relevant checks "
                "without modifying files. Verify formats, edge cases, and completion "
                "claims against the specification. Return findings with file "
                "references and observed evidence, checks performed, and anything "
                "not verified. Do not assume the implementer's report is correct."
            ),
        },
    ]
