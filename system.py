import shared
import whiptail

class SystemData:
	def __init__(self):
		self.config = None

	def reload(self, quiet=False):
		self.config = shared.jsonLoad("/data/.config/main.json", silent=quiet)
		self.colorconf = shared.jsonLoad("/data/.config/colorconf.json", silent=quiet)
		self.build = {
			"number": open("/buildct").read().replace("\n",""),
			"time": open("/buildtm").read().replace("\n", "")}

	def init(self):
		self.config = shared.jsonLoad("/data/.config/main.json", silent=False)
		self.colorconf = shared.jsonLoad("/data/.config/colorconf.json", silent=False)
		self.build = {
			"number": open("/buildct").read().replace("\n",""),
			"time": open("/buildtm").read().replace("\n", "")}


	def set(self, location, value):
		try:
			l = [i.replace("/", "") for i in location.split("/")]
			cl = ""
			if l[0] == "main":
				cl = self.config
			elif l[0] == "color":
				cl = self.colorconf
#			elif l[0] == "build":
#				cl = self.build
			else:
				raise ValueError("No base location {0}".format(l[0]))
			del l[0]
			index = 0
			for a in l:
				if a == len(l) - 1:
					# last one
					print("change this")
					print(cl[a])
					cl[a] = value
					return
				cl = cl[a]


		except Exception as e:
			shared.logger.error("Cannot set system key <{0}> due to <{1}>".format(location, e))
			raise e
			return

	def get(self, location):
		try:
			l = [i.replace("/", "") for i in location.split("/")]
			cl = ""
			if l[0] == "main":
				cl = self.config
			elif l[0] == "color":
				cl = self.colorconf
			elif l[0] == "build":
				cl = self.build
			else:
				raise ValueError("No base location {0}".format(l[0]))
			del l[0]
			for a in l:
				cl = cl[a]

			return cl

		except Exception as e:
			shared.logger.error("Cannot get system key <{0}> due to <{1}>".format(location, e))
			raise e
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

