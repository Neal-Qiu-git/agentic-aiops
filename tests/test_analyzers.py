from aiops.analyzers.anomaly import AnomalyAnalyzer

def test_normal():
    a = AnomalyAnalyzer()
    r = a.analyze({"cpu":{"usage_percent":30},"memory":{"used_percent":50},"disk":[{"used_percent":40,"mount":"/"}],"load":{"load1":0.5},"swap":{"used_percent":0}})
    assert r["total"] == 0

def test_critical():
    a = AnomalyAnalyzer()
    r = a.analyze({"cpu":{"usage_percent":95}})
    assert r["critical"] >= 1
