from helium import click, Button, Text, find_all, S


class TestMaxes:
    def test_lift_maxes(self, driver_login):
        click(Button("Lift Maxes"))
        assert Text("Maxes").exists()
        assert Button("Submit").exists()
        assert Text("Max Charts").exists
        charts = find_all(S("canvas", below=Text("Max Charts")))
        assert len(charts) == 4
