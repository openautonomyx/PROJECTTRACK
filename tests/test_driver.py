from projecttrack.driver import ProjectDriver

def test_driver_initialization():
    driver = ProjectDriver("TestProject")
    assert driver.name == "TestProject"
    assert driver.status == "initialized"