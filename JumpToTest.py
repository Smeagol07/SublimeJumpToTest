import sublime, sublime_plugin, os.path
import re

class JumpToTest(sublime_plugin.TextCommand):

  potential_files = []

  def run(self, edit):
    if self.view.file_name() == None:
      print ("Curent file not available")
      return

    self.potential_files = []
    self.settings = sublime.load_settings('JumpToTest.sublime-settings')
    self.user_settings = sublime.load_settings('Preferences.sublime-settings')

    desiredfile = ""
    currentfile = self.view.file_name().split(os.sep)[-1]
    extension = currentfile.split(".")[-1]

    if currentfile.endswith("_test." + extension):
      desiredfile = currentfile[:-8] + "." + extension
    else:
      desiredfile = currentfile[:-3] + "_test." + extension

    file_path = self.get_potential_files(desiredfile)

    if len(file_path) == 0:
      print ("File '%s' not found" % (desiredfile))
      return

    if len(file_path) == 1 and os.path.isfile(file_path[0]):
      sublime.active_window().open_file(file_path[0])
    else:
      self.view.window().show_quick_panel(file_path, self.open_file)

  def get_potential_files(self, file_name):
    if self.get_settings('jtt_always_lookup_in_all_files') == False:
      self.potential_files = self.getOpenFiles(file_name)
    if len(self.potential_files) == 0:
      self.potential_files = self.getAllFiles(file_name)
    return self.potential_files

  def getOpenFiles(self, file_name):
    results = []
    open_files = sublime.active_window().views()
    for file in open_files:
      if (file.file_name().endswith(file_name)):
        results += [file.file_name()]

    return results

  def getAllFiles(self, file_name):
    results = []
    directories = self.view.window().folders()
    for directory in directories:
      for dirname, _, files in self.walk(directory):
        for file in files:
          fileName = dirname + os.sep + file
          if re.search(file_name, fileName):
            results += [fileName]

    return results

  def walk(self, directory):
    for dir, dirnames, files in os.walk(directory):
        dirnames[:] = [dirname for dirname in dirnames]
        yield dir, dirnames, files

  def open_file(self, selected_index):
    if selected_index != -1:
      file = self.potential_files[selected_index]
      print("Opening file '%s'" % (file))
      self.view.window().open_file(file)

  def get_settings(self, option):
    # view specific settings
    if self.view.settings().get(option) != None:
      return self.view.settings().get(option)
    # user global sttings
    if self.user_settings.get(option) != None:
      return self.user_settings.get(option)
    #default plugin settings
    return self.settings.get(option)