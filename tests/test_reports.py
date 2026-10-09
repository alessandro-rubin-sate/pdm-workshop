import polars as pl
import pytest

from pdm_workshop.cli import main
from pdm_workshop.reports import fleet_summary, load_feature_table, machine_report


@pytest.fixture(scope="module")
def table() -> pl.DataFrame:
    return load_feature_table()


def test_summary_has_one_row_per_machine(table):
    summary = fleet_summary(table)
    assert summary.height == table["machine_id"].n_unique()
    assert summary["machine_id"].is_sorted()


def test_report_covers_the_requested_period_in_five_bands(table):
    report = machine_report(table, "M07", hours=100)

    assert report["hours_before_end"].to_list() == [100.0, 80.0, 60.0, 40.0, 20.0]
    # One snapshot every two hours: fifty of them in a hundred hours.
    assert report["snapshots"].sum() == 50


def test_report_shows_the_machine_drifting_from_its_start(table):
    report = machine_report(table, "M07", hours=100)
    assert report["rms_rel"][-1] > report["rms_rel"][0]


def test_report_rejects_what_it_cannot_answer(table):
    with pytest.raises(ValueError, match="unknown machine"):
        machine_report(table, "M99")
    with pytest.raises(ValueError, match="positive"):
        machine_report(table, "M07", hours=0)


def test_command_prints_a_report(capsys):
    assert main(["report", "--machine", "M07", "--hours", "48"]) == 0
    assert "hours_before_end" in capsys.readouterr().out


def test_command_answers_a_wrong_machine_with_a_message_not_a_traceback(capsys):
    with pytest.raises(SystemExit) as exit_info:
        main(["report", "--machine", "M99"])

    assert exit_info.value.code == 2
    assert "unknown machine 'M99'" in capsys.readouterr().err
