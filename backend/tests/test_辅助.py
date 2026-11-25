from app.services import 时间, 校验, 目录, 统计, 说明, 装载, 夹具, 结栏, 贯验


def test_解析观测时():
    t = 时间.解析时("2026-11-24T08:00:00Z")
    assert t.year == 2026


def test_栏规补丁拒倒挂():
    out = 目录.改栏规({"PM25下限": "90", "PM25上限": "10"})
    assert "错误" in out


def test_仓情含命运词典():
    info = 说明.仓情()
    assert "已入栏" in info["命运词典"]
    assert len(info["阶段说明"]) == 4


def test_装载批次可查():
    装载.装一批(夹具.读取("入栏成汇总样例"))
    assert 目录.装载批次列表()
    assert 统计.报文命运()


def test_观测时坏格式驳回():
    体 = {
        "报文": [{
            "报文编号": "bad-time-1",
            "站点键": "站-河东",
            "指标键": "PM25",
            "读数": 20,
            "观测时": "不是时间",
        }]
    }
    assert 装载.装一批(体)["驳回"] == 1


def test_摘要错误截断():
    s = 校验.摘要错误([f"e{i}" for i in range(12)], 上限=3)
    assert "另有" in s


def test_结栏预览与贯验快照():
    装载.装一批(夹具.读取("入栏成汇总样例"))
    prev = 结栏.预览结栏()
    assert prev["在栏"] == 3
    assert len(prev["将汇总组"]) == 2
    snap = 贯验.只读快照()
    assert "是否对齐" in snap
