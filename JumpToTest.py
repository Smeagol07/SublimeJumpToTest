import sublime, sublime_plugin, os.path
import re, json

class JumpToTest(sublime_plugin.TextCommand):

  potential_files = []
  pattern_name = None

  def run(self, edit, pattern_name = None):
    if self.view.file_name() == None:
      print ("Curent file not available")
      return

    self.potential_files = []
    self.pattern_name = pattern_name
    self.settings = sublime.load_settings('JumpToTest.sublime-settings')
    self.user_settings = sublime.load_settings('Preferences.sublime-settings')

    target_file_name = self.get_target_file_name()

    if target_file_name == None:
      print("Sorry, nothing matched that file")
      return

    file_path = self.get_potential_files(target_file_name)

    if len(file_path) == 0:
      print ("File '%s' not found" % (target_file_name))
      return

    if len(file_path) == 1 and os.path.isfile(file_path[0][2]):
      sublime.active_window().open_file(file_path[0][2])
    else:
      self.view.window().show_quick_panel(file_path, self.open_file)

  def get_potential_files(self, file_name):
    if self.get_settings('jtt_always_lookup_in_all_files') == False:
      self.potential_files = self.get_open_files(file_name)
    if len(self.potential_files) == 0:
      self.potential_files = self.get_all_files(file_name)
    return self.potential_files

  def get_open_files(self, file_name):
    results = []
    open_files = sublime.active_window().views()
    for file in open_files:
      if (file.file_name().endswith(file_name)):
        results += [self.get_file_item(file.file_name())]

    return results

  def get_target_file_name(self):
    current_file_full_path = self.view.file_name()
    current_file_name = self.view.file_name().split(os.sep)[-1]
    target_file_name = None;
    patterns = self.get_settings('jtt_pattens')
    for pattern in patterns:
      if self.pattern_name != None and self.pattern_name != pattern['name']:
        # skip pattern if we aiming by name
        continue

      if pattern['re_check_full_path'] == True:
        check_name = current_file_full_path
      else:
        check_name = current_file_name

      if re.search(pattern['re_check_type'], check_name) == None:
        print("Pattern %s not matched" % pattern['name'])
        continue
      else:
        print("Pattern %s matched!" % pattern['name'])

      if re.search(pattern['re_is_test'], check_name) == None:
        print("This is not test file")
        target_file_name = re.sub(pattern['re_to_test'][0], pattern['re_to_test'][1], check_name)
      else:
        print("This is test file")
        target_file_name = re.sub(pattern['re_from_test'][0], pattern['re_from_test'][1], check_name)
      break

    return target_file_name

  def get_all_files(self, file_name):
    results = []
    directories = self.view.window().folders()
    for directory in directories:
      for dirname, _, files in self.walk(directory):
        for file in files:
          full_file_name = dirname + os.sep + file
          if re.search(file_name, full_file_name):
            results += [self.get_file_item(full_file_name)]

    return results

  def walk(self, directory):
    for dir, dirnames, files in os.walk(directory):
        dirnames[:] = [dirname for dirname in dirnames]
        yield dir, dirnames, files

  def open_file(self, selected_index):
    if selected_index != -1:
      file = self.potential_files[selected_index][2]
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

  def get_file_item(self, file_name):
    return [file_name.split(os.sep)[-1], os.sep.join(file_name.split(os.sep)[-5:]), file_name]
