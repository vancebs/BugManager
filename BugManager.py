from script.BugManager import BugManager


def launch():
    bm = BugManager()
    bm.launch()


def test_local_alm():
    from script.model.local_alm.spider.ProjectSpider import ProjectSpider
    from script.model.local_alm.spider.GeneralSpider import GeneralSpider

    gs = GeneralSpider()
    gs.sync()

    ps = ProjectSpider('/TCT/GApp/Gallery')
    ps.sync()


def test_alm():
    pass

if __name__ == "__main__":
    launch()
    # test_local_alm()
