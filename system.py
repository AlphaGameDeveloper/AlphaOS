import shared
import whiptail
import json


class SystemData:
    def __init__(self):
        self.config = None
        self.registries = {}
        self.mounts = None
        shared.logger.step("System Registry")

        self.build = {
            "number": open("/buildct").read().replace("\n", ""),
            "time": open("/buildtm").read().replace("\n", "")}

        self.reload(quiet=False, initial=True)
        shared.logger.substep("All Done")

    def reload(self, quiet=False, initial=False):
        if initial:
            shared.logger.substep("Read registry mounts configuration")
        self.mounts = shared.jsonLoad("/data/.config/registry.json", silent=quiet)["mounts"]

        if initial:
            shared.logger.substep("Mount system registries")

        for mount in self.mounts:
            if initial:
                shared.logger.substep(
                    f"Mount system registry {mount['path']} at /{mount['point']}")
            self.registries[mount["point"]] = shared.jsonLoad(mount["path"], silent=quiet)

        self.registries["build"]= {
            "number": open("/buildct").read().replace("\n", ""),
            "time": open("/buildtm").read().replace("\n", "")}

    def init(self):
        shared.logger.warn(
            "SystemData.init is depricated!  Please use SystemData.reload instead!")

    def set(self, location, value):
        try:
            location_parts = [i.replace("/", "") for i in location.split("/")]
            current_location = ""
            if location_parts[0] == "main":
                current_location = self.config
            elif location_parts[0] == "color":
                current_location = self.colorconf
# elif l[0] == "build":
# cl = self.build
            else:
                raise ValueError("No base location {0}".format(location_parts[0]))
            del location_parts[0]
            index = 0
            for a in location_parts:
                if a == len(l) - 1:
                    # last one (???????????)
                    print("change this")
                    print(current_location[a])
                    current_location[a] = value
                    return
                current_location = current_location[a]
        except ValueError:
            return None
        except Exception as e:
            shared.logger.error("Cannot set system key <{0}> due to <{1}>".format(location, repr(e)))
            return None
            
    def save(self):
        with open("/data/.config/main.json", "w") as f:
            json.dump(self.config["main"], f)
        with open("/data/.config/colorconf.json", "w") as f:
            json.dump(self.colorconf, f)

    def get(self, location):
        try:
            location_parts = [i.replace("/", "") for i in location.split("/") if i.strip() != ""]
            current_location = ""
            try:
                current_location = self.registries[location_parts[0]]
            except NameError:
                shared.logger.error("No base location {0}" % location_parts[0])
                return None
            
            del location_parts[0]
            for location in location_parts:
                try:
                    location = int(location)
                except ValueError:
                    pass # ok, can't do that!
                current_location = current_location[location]

            return current_location

        except Exception as e:
            shared.logger.error("Cannot get system key <{0}>".format(location))
            return


class SystemHandler:
    def __init__(self):
        pass

    def system(self, ctx, args):
        del args[0]
        if len(args) == 0:
            print("Usage: system <command> <subcommand>")
            print("|  Command  |  Subcommands")
            print("+-----------+------------")
            print("|   passwd  |  change,forcereset")
            return 0

        args[0] = args[0].lower()

        if args[0] == "passwd":
            if len(args) == 2:
                args[1] = args[1].lower()
                if args[1] == "forcereset":
                    pass


data = SystemData()
data.init()

handler = SystemHandler()
