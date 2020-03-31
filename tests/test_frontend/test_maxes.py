from helium import click, Button, Text, find_all, S, Link


class TestMaxes:
    def test_lift_maxes(self, driver_login):
        click(Link("Training Max"))
        assert Text("Training Max").exists()
        assert Button("Submit").exists()
        assert Text("Charts").exists
        charts = find_all(S("canvas", below=Text("Charts")))
        assert len(charts) == 4
