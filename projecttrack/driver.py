class ProjectDriver:
    def __init__(self, name):
        self.name = name
        self.status = "initialized"

    def start(self):
        self.status = "running"
        print(f"Project '{self.name}' started.")

    def stop(self):
        self.status = "stopped"
        print(f"Project '{self.name}' stopped.")

def main():
    driver = ProjectDriver("ExampleProject")
    driver.start()

if __name__ == "__main__":
    main()