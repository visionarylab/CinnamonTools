#!/usr/bin/python3

import sys
import os
import subprocess
from argparse import ArgumentParser

repo_folder = os.path.realpath(os.path.abspath(os.path.join(
    os.path.normpath(os.path.join(os.getcwd(), *([".."] * 2))))))

# The modules folder is two levels up from were this script is run (the repository folder).
# "tools/cinnamon_tools_python_modules"
tools_folder = os.path.join(repo_folder, "tools")

if tools_folder not in sys.path:
    sys.path.insert(0, tools_folder)

from gi.repository import GLib
from cinnamon_tools_python_modules import localized_help_modules
from cinnamon_tools_python_modules import mistune
from cinnamon_tools_python_modules.pyuca import Collator
from cinnamon_tools_python_modules.locale_list import locale_list

pyuca_collator = Collator()
md = mistune.Markdown()

XLET_DIR = os.path.dirname(os.path.abspath(__file__))
XLET_UUID = str(os.path.basename(XLET_DIR))

xlet_meta = localized_help_modules.XletMetadata(
    os.path.join(XLET_DIR, "files", XLET_UUID)).xlet_meta

if xlet_meta is None:
    quit()

tags = localized_help_modules.HTMLTags()
translations = localized_help_modules.Translations()
# Set current_language to global every time that needs to be assigned.
current_language = "en"


def _(aStr):
    trans = translations.get([current_language]).gettext

    if not aStr.strip():
        return aStr

    current_language_stats["total"] = current_language_stats["total"] + 1

    if trans:
        result = trans(aStr)

        try:
            result = result.decode("utf-8")
        except:
            result = result

        if result != aStr:
            current_language_stats["translated"] = current_language_stats["translated"] + 1
            return result

    return aStr


# Base information about the xlet (Description, features, dependencies, etc.).
# This is used by the xlet README and the xlets help file.
# Returns a "raw markdown string" that it is used "as-is" for the README creation,
# but it's converted to HTML when used by the help file.
#
# Separate each "block" with an empty space, not a new line. When joining the
# string with a new line character, an empty space will add one line, but a
# new line character will add two lines. This is just to keep the README content
# somewhat homogeneous.
def get_content_base(for_readme=False):
    return "\n".join([
        "## %s" % _("Description"),
        "",
        # TO TRANSLATORS: MARKDOWN string. Respect formatting.
        _("Applet based on two gnome-shell extensions ([Todo list](https://github.com/bsaleil/todolist-gnome-shell-extension) and [Section Todo List](https://github.com/tomMoral/ToDoList)). It allows to create simple ToDo lists from a menu on the panel."),
        "",
        "## %s" % _("Applet usage and features"),
        "",
        _("The usage of this applet is very simple. Each task list is represented by a sub menu and each sub menu item inside a sub menu represents a task."),
        "",
        # TO TRANSLATORS: MARKDOWN string. Respect formatting.
        "- %s" % ("To add a new tasks list, simply focus the **New tasks list...** entry, give a name to the tasks list and press <kbd>Enter</kbd>." if for_readme else _(
            "To add a new tasks list, simply focus the **New tasks list...** entry, give a name to the tasks list and press [[Enter]].")),
        # TO TRANSLATORS: MARKDOWN string. Respect formatting.
        "- %s" % ("To add a new task, simply focus the **New task...** entry, give a name to the task and press <kbd>Enter</kbd>." if for_readme else _(
            "To add a new task, simply focus the **New task...** entry, give a name to the task and press [[Enter]].")),
        "- %s" % _("All tasks lists and tasks can be edited in-line."),
        "- %s" % _("Tasks can be marked as completed by changing the checked state of their sub menu items."),
        "- %s" % _("Each tasks list can have its own settings for sorting tasks (by name and/or by completed state), remove task button visibility and completed tasks visibility."),
        "- %s" % _("Each tasks list can be saved as individual TODO files and also can be exported into a file for backup purposes."),
        "- %s" % _("Tasks can be reordered by simply dragging them inside the tasks list they belong to (only if all automatic sorting options for the tasks list are disabled)."),
        "- %s" % _("Tasks can be deleted by simply pressing the delete task button (if visible)."),
        "- %s" % _("Colorized priority tags support. The background and text colors of a task can be colorized depending on the @tag found inside the task text."),
        "- %s" % _("Configurable hotkey to open/close the menu."),
        "- %s" % _("Read the tooltips of each option on this applet settings window for more details."),
    ])


# The real content of the HELP file.
def get_content_extra():
    return md("{}".format("\n".join([
        "## %s" % _("Keyboard shortcuts"),
        _("The keyboard navigation inside this applet menu is very similar to the keyboard navigation used by any other menu on Cinnamon. But it's slightly changed to facilitate tasks and sections handling and edition."),
        "",
        "### %s" % _("When the focus is on a task"),
        # TO TRANSLATORS: MARKDOWN string. Respect formatting.
        "- " + _("[[Ctrl]] + [[Spacebar]]: Toggle the completed (checked) state of a task."),
        # TO TRANSLATORS: MARKDOWN string. Respect formatting.
        "- " + _("[[Shift]] + [[Delete]]: Deletes a task and focuses the element above of the deleted task."),
        # TO TRANSLATORS: MARKDOWN string. Respect formatting.
        "- " + _("[[Alt]] + [[Delete]]: Deletes a task and focuses the element bellow the deleted task."),
        # TO TRANSLATORS: MARKDOWN string. Respect formatting.
        "- " + _("[[Ctrl]] + [[Arrow Up]] or [[Ctrl]] + [[Arrow Down]]: Moves a task inside its tasks list."),
        # TO TRANSLATORS: MARKDOWN string. Respect formatting.
        "- " + _("[[Insert]]: Will focus the **New task...** entry of the currently opened task section."),
        "",
        "### %s" % _("When the focus is on a task section"),
        # TO TRANSLATORS: MARKDOWN string. Respect formatting.
        "- " + _("[[Arrow Left]] and [[Arrow Right]]: If the tasks list (sub menu) is closed, these keys will open the sub menu. If the sub menu is open, these keys will move the cursor inside the sub menu label to allow the edition of the section text."),
        # TO TRANSLATORS: MARKDOWN string. Respect formatting.
        "- " + _("[[Insert]]: Will focus the **New task...** entry inside the task section. If the task section sub menu isn't open, it will be opened."),
        "",
        # TO TRANSLATORS: MARKDOWN string. Respect formatting.
        "### %s" % _("When the focus is on the **New task...** entry"),
        # TO TRANSLATORS: MARKDOWN string. Respect formatting.
        "- " + _("[[Ctrl]] + [[Spacebar]]: Toggles the visibility of the tasks list options menu."),
        "",
        "## %s" % _("Known issues"),
        # TO TRANSLATORS: MARKDOWN string. Respect formatting.
        "- " + _("**Hovering over items inside the menu doesn't highlight menu items nor sub menus:** This is actually a desired feature. Allowing the items to highlight on mouse hover would cause the entries to loose focus, resulting in the impossibility to keep typing text inside them and constantly forcing us to move the mouse cursor to regain focus."),
        "- **%s** %s" % (_("Task entries look wrong:"), _(
            # TO TRANSLATORS: MARKDOWN string. Respect formatting.
            "Task entries on this applet have the ability to wrap its text in case one sets a fixed width for them. They also can be multi line ([[Shift]] + [[Enter]] inside an entry will create a new line). Some Cinnamon themes, like the default Mint-X family of themes, set a fixed width and a fixed height for entries inside menus. These fixed sizes makes it impossible to programmatically set a desired width for the entries (at least, I couldn't find a way to do it). And the fixed height doesn't allow the entries to expand, completely breaking the entries capability to wrap its text and to be multi line.")),
        "",
        "### %s" % _("This is how entries should look like"),
        "",
        "<img class=\"correct-entries-styling\" alt=\"%s\">" % _("Correct entries styling"),
        "",
        "### %s" % _("This is how entries SHOULD NOT look like"),
        "",
        "<img class=\"incorrect-entries-styling\" alt=\"%s\">" % _("Incorrect entries styling"),
        "",
        # TO TRANSLATORS: MARKDOWN string. Respect formatting.
        _("The only way to fix this (that I could find) is by editing the Cinnamon theme that one is using and remove those fixed sizes. The CSS selectors that needs to be edited are **.menu StEntry**, **.menu StEntry:focus**, **.popup-menu StEntry** and **.popup-menu StEntry:focus**. Depending on the Cinnamon version the theme was created for, one might find just the first two selectors or the last two or all of them. The CSS properties that need to be edited are **width** and **height**. They could be removed, but the sensible thing to do is to rename them to **min-width** and **min-height** respectively. After editing the theme's file and restarting Cinnamon, the entries inside this applet will look and work like they should."),
    ])
    ))


# I have to add the custom CSS code separately and not include it directly in the
# HTML templates because the .format() function breaks when there is CSS code present
# in the string.
def get_css_custom():
    return "/* Specific CSS code for specific HELP files */"


# Inject some custom JavaScript code to be executed when page finalyzes to load.
def get_js_custom():
    return """
Array.prototype.slice.call(document.getElementsByClassName("incorrect-entries-styling")).forEach(function(aEl) {
aEl.setAttribute("src", "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAdIAAAFxCAMAAADwNtlEAAADAFBMVEX+/v7+/v309PT09PT09PT09PT09PT09PT09PTz8/Px8fHy8vLy8vLw8PDv7+/u7u7u7u7t7e3t7e3t7e3s7Ozs7Ozt7e3t7e3u7u7u7u7v7+/v7+/w8PDv7+/v7+/u7u7u7u7r6+vr6+vq6urq6urq6uro6Ojo6Ojm5ubk5OTj4+Pi4uLh4eHf39/f39/d3d3c3Nzc3Nzc3Nzb29va2trZ2dnY2NjX19fV1dXU1NTT09PT09PS0tLS0tLR0dHR0dHQ0c/Q08zN08fLy8rJycjGxsbDw8PCwsLBwcG+vr67u7u/uL/codzcodzdod3codzNp82zs7OwsLCtra2oqKijo6Ofn5+dnZ2cnJybm5ubm5uampqYmJiTk5OPj4+KioqFkJN2mapMk9U6j+ZLi8+AgoR9fX13d3dxcXFtbW1lZWViYmJgYGBeXl5cXFxZWVlWVlZRUVFMTExHR0dERERBQUE+Pj47Ozs2NjYzMzMwMDAsLCwrKyspKSkiIiIdHR0YGBgTExMQEBAMDAwJCQkHBwcFBQUDAwMCAgIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANAgHGBgTHAgHIAADIAADIAADIAADIAADIAADIAADIAADIAADIAADIAADIAADLAAD+AAD/AAD/AAD/AAD/AAD/AAD/AAD/AAD/AAD/AAD8BAPpy0jozEnozEnozEnozEnozEnmy0rly0vky0vly0vmy0rozEnozEnpzUjp0EPr1jvs2zXt4C7w6CL4+gn5+gj5+wf8/AT9/gL//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD///+EyTVTAAABAHRSTlP///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////8AU/cHJQAAAAlwSFlzAAALEwAACxMBAJqcGAAAGiBJREFUeAHs0TERAkEMAEBMxEDauGHOxj3FUT7aoT0YDORn18Le3lyMUqUo/QulKFW6HrS2fkpfozIaI+t+fpWOaI+xl64K2qvnVnpk0F4eW+kMLmAqVYpSlKIUpUpRilKUolQpSlGKUpR2phSlSjmVKlX6YbdsVhtHHiD+FPUCQf6YTJKFzJ/JYlgm4DiJfZNjOX8WOzrpQ7ITWS1Llrrr4XcVuZGs7GEuJoaZOjRUyQVF/6DxKes3UsHn/87CYopPVHvZb6RtrVhp/tNII87qZPGEtr57qdwGj5+B1OETLrydjE2U+lNlPQy8rZQmxsr/VZC6QkhmQkx/GqlxUQcj+mhLsEgKmp+A9EGtgJCFoLwHAJs2Rjmzt7cJ4NM8IaS98fz/payhcYyHN+YLgIcglan7FZjFRb6x3i/uStA/q7y+zP1RhdOUZI4DDcghjDFgvGxl5l0CQo4imdmDlcycM6Bnb+XWOQeA2ixZ3MCiHNY7WjVBM5KppVfoIhrzQpoYkA8IGAAwUjWA4OIMpUaMTgipce9u4jiO7NvO8ZCO8pWf0cNQMQh3zxCcn28YGtofIN2HlmDiOTjQpaTdBQCPcrOj6EJQrlZk/haQszJP3JgBANSmEzG83nFZ72jXBFUQkqP9Cl1szOvLvIMZd6gOmFxjxHjseSYAbHlNnIz6k0Akwh31cDykMGDMmGJCacLoQdB65WtX+0OkOvTooy1LMVv08V3RxHXOGQRDIGEEvNEp88ebH5JXABrmR0HBqFPvaNUg6AFhxfq5LjbmjbkCFhTAhKoDhHyCxa0iuQDgc0qcFlNN9EhIp5ucZI7uhkzmZxAUlN+g/SFSHdZIn6MoMvGuu0BRfDOpDGBNB4JL4JUO4NODyUr3AJpmQcq/GjtaNQgugBdG7wPqYmPejB40UnZwo7Ie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");
});
Array.prototype.slice.call(document.getElementsByClassName("correct-entries-styling")).forEach(function(aEl) {
aEl.setAttribute("src", "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAdIAAAGhCAMAAADiCMVrAAADAFBMVEX+/v7+/v329vb19fX19fX09PT09PTz8/Pz8/Pz8/Py8vLx8fHx8fHx8fHw8PDw8PDv7+/v7+/v7+/u7u7u7u7u7u7t7e3t7e3s7Ozs7Ozr6+vr6+vr6+vq6urq6urq6urp6enp6eno6Ojo6Ojn5+fm5ubl5eXl5eXk5OTj4+Pi4uLi4uLh4eHh4eHg4ODf39/f39/e3t7e3t7d3d3c3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzb29vb29va2tra2trZ2dnY2NjX19fV1tXV1dTVz9XcodvcodzcoNzcodzco9zS0dLS0tLS0tLS0tLP0c7Ly8vFxcXCwsK/v7+4uLizs7OwsLCtra2oqKijo6OgoKCdnZ2cnJybm5ubm5uampqYmJiUlJSOl5p5m6xIktk6j+ZQjs+NjY2KioqHh4eBgYF6enp0dHRtbW1mZmZjY2NiYmJfX19eXl5cXFxZWVlYWFhWVlZSUlJOTk5LS0tISEhFRUVDQ0NAQEA8PDw6Ojo3Nzc0NDQyMjIvLy8uLi4sLCwrKysqKiopKSkiIiIeHh4cHBwYGBgUFBQREREODg4LCwsJCQkICAgHBwcFBQUDAwMCAgIBAQEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAQEBAQEAAAABAQF7AgG+BAPGBQPHBAPHAgHIAADIAADIAADIAADIAADIAADIAADIAADIAADnAAD/AAD/AAD/AAD/AAD/AAD/AAD/AAD/AAD/AAD/AAD/AAD+AgH9BAP8BQT3LhPooz7prkDowEbny0rnzErozEnozEnozEnozEnozEnozEnozEnozEnozEnozEnozEnozEnpzUnpz0X4+gn5+wj+/gH//wH//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD//wD///8I4BQsAAABAHRSTlP///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////8AU/cHJQAAAAlwSFlzAAALEwAACxMBAJqcGAAAHpdJREFUeAHsme1LI8u2xvf5NOCGQBhoCgQJGFExjIifZBjmxW/DmHTMu6KGzSGmO92JJuYlMS/daR/un31vdaVXn07veEbvnjhxph6YdK9Va1U9VT90JPXH//5ikpJIJVIpiVRKIpWSSKUkUolU6lUi7bfupF6xWv0Q0v8p7K2zVyyp9b0c5pAW2KuXVCGItL/HXr2k9gYBpM119uoltd4MIL1lv4CkbiVSiVRKIpWSSKUkUimJVCKVkkilJFIpiVRKIpVIpSRSqdeMVEoilZJIpSRSKYlUIpWCRLrKkkilJNIezhbnTDvHfqrI2WJJpHXMVHoy0hYKzFc5z8L6VBtOB0b6ZyDVkGcJfTztZET4xRltshN9MJ1m2emD8bsg1bpdG6NuN/dkpLEE86XCYGF1YfdtZH4C0vRDgzETVg+O6sbXqDJ1glGzyd3UkP31kZI6qLjnYQ6nQ32PsULXmrSL4uAOuqitezEdpvtBRbkhgAmb0wmQYrFTjr4y4BPu84ap2poOKycNe1hdZ2zzejAdVHeZEAVlWJ9ZEXbK9xFu6yHLwxK58GcJ2DORdZdPMwMGD2PDhxPWxdU6c6Wi9bshVa1GbYgaSz3AMEdn7sHttmHGKA4ipaJSD31dY3Pan6ISZ1w6pu0xunHeYNfrgNU0gAJjNfS1Dv10U7DRgnk0Rvk/PsJtPTiGCaieC2oM2NueTjZYASM2+2BZ3HCQnVNdzzKuexytDtLN09K5q2IqtjykLMZiBdyzU0yzLLbJeije4jZO8TxSSuqEJqCSg2F5m31ykGVHExR4g8nYAHeMNaG5+fTnrzYOeGkg4B9dtDb+4yPUxkOO2YQ+M+A3BuydosHYFbqMZfDAZ6ojz0oYOADKfNhAbnWQxlS93el07q6TG8tDmmtPAExY/A7on62zHrqYvmcU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");
});
"""


class Main():

    def __init__(self):
        self.html_templates = localized_help_modules.HTMLTemplates()
        self.html_assets = localized_help_modules.HTMLInlineAssets(repo_folder=repo_folder)
        self.compatibility_data = localized_help_modules.get_compatibility(
            xlet_meta=xlet_meta,
            for_readme=False
        )
        self.lang_list = []
        self.sections = []
        self.options = []

        try:
            contributors_file = open(os.path.join(XLET_DIR, "CONTRIBUTORS.md"), "r")
            contributors_rawdata = contributors_file.read()
            contributors_file.close()
            self.contributors = self.html_templates.boxed_container.format(md(contributors_rawdata))
        except Exception as detail:
            print(detail)
            self.contributors = None

        try:
            changelog_file = open(os.path.join(XLET_DIR, "CHANGELOG.md"), "r")
            changelog_rawdata = changelog_file.read()
            changelog_file.close()
            self.changelog = self.html_templates.boxed_container.format(md(changelog_rawdata))
        except Exception as detail:
            print(detail)
            self.changelog = None

    def create_html_document(self):
        for lang in self.lang_list:
            global current_language
            current_language = lang

            global current_language_stats
            current_language_stats = {
                "total": 0,
                "translated": 0
            }

            if current_language == "en":
                localized_help_modules.create_readme(
                    xlet_dir=XLET_DIR,
                    xlet_meta=xlet_meta,
                    content_base=get_content_base(for_readme=True)
                )

            only_english = md("<div style=\"font-weight:bold;\" class=\"alert alert-info\">{0}</div>".format(
                _("The following two sections are available only in English."))
            )

            compatibility_disclaimer = "<p class=\"text-danger compatibility-disclaimer\">{}</p>".format(
                _("Do not install on any other version of Cinnamon.")
            )

            compatibility_block = self.html_templates.bt_panel.format(
                context="success",
                custom_class="compatibility",
                title=_("Compatibility"),
                content=self.compatibility_data + "\n<br/>" + compatibility_disclaimer,
            )

            section = self.html_templates.locale_section_base.format(
                language_code=current_language,
                hidden="" if current_language is "en" else " hidden",
                introduction=self.get_introduction(),
                compatibility=compatibility_block,
                content_base=md(get_content_base(for_readme=False)),
                content_extra=get_content_extra(),
                localize_info=self.get_localize_info(),
                only_english=only_english,
            )

            option = self.get_option()

            # option could be None if the the language has no endonym or if the amount
            # of translated strings is lower than 50% of the total translatable strings.
            if option is not None:
                self.sections.append(section)
                self.options.append(option)

        html_doc = self.html_templates.html_doc.format(
            # This string doesn't need to be translated.
            # It's the initial title of the page that it's always in English.
            title="Help for {xlet_name}".format(xlet_name=xlet_meta["name"]),
            # WARNING!!! Insert the inline files (.css and .js) AFTER all string formatting has been done.
            # CSS code interferes with formatting variables. ¬¬
            js_localizations_handler=self.html_assets.js_localizations_handler if
            self.html_assets.js_localizations_handler else "",
            css_bootstrap=self.html_assets.css_bootstrap if self.html_assets.css_bootstrap else "",
            css_tweaks=self.html_assets.css_tweaks if self.html_assets.css_tweaks else "",
            css_base=self.html_templates.css_base,
            css_custom=get_css_custom(),
            options="\n".join(sorted(self.options, key=pyuca_collator.sort_key)),
            sections="\n".join(self.sections),
            contributors=self.contributors if self.contributors else "",
            changelog=self.changelog if self.changelog else "",
            js_custom=get_js_custom()
        )

        localized_help_modules.save_file(path=self.help_file_path,
                                         data=html_doc,
                                         creation_type=self.creation_type)

    def do_dummy_install(self):
        podir = os.path.join(XLET_DIR, "files", XLET_UUID, "po")
        done_one = False
        dummy_locale_path = os.path.join("../../", "tmp", "locales", XLET_UUID)

        for root, subFolders, files in os.walk(podir, topdown=False):
            for file in files:
                pofile_path = os.path.join(root, file)
                parts = os.path.splitext(file)

                if parts[1] == ".po":
                    try:
                        try:
                            lang_name = locale_list[parts[0]]["name"]
                        except:
                            lang_name = ""

                        localized_help_modules.validate_po_file(
                            pofile_path=pofile_path,
                            lang_name=lang_name,
                            xlet_meta=xlet_meta
                        )
                    finally:
                        self.lang_list.append(parts[0])
                        this_locale_dir = os.path.join(dummy_locale_path, parts[0], "LC_MESSAGES")
                        GLib.mkdir_with_parents(this_locale_dir, 0o755)
                        subprocess.call(["msgfmt", "-c", pofile_path, "-o",
                                         os.path.join(this_locale_dir, "%s.mo" % XLET_UUID)])
                        done_one = True

        if done_one:
            print("Dummy install complete")

            if len(self.lang_list) > 0:
                translations.store(XLET_UUID, dummy_locale_path, self.lang_list)

            # Append english to lang_list AFTER storing the translations.
            self.lang_list.append("en")
            self.create_html_document()
        else:
            print("Dummy install failed")
            quit()

    def get_language_stats(self):
        stats_total = str(current_language_stats["total"])
        stats_translated = str(current_language_stats["translated"])

        return int(100 * float(stats_translated) / float(stats_total))

    def get_option(self):
        try:
            endonym = locale_list[current_language]["endonym"]
            language_name = locale_list[current_language]["name"]
        except:
            endonym = None
            language_name = None

        if current_language == "en" or (endonym is not None and self.get_language_stats() >= 50):
            # Define them first before self.get_language_stats() is called so these
            # strings are also counted.
            xlet_help = _("Help")
            xlet_contributors = _("Contributors")
            xlet_changelog = _("Changelog")
            title = _("Help for %s") % xlet_meta["name"]

            return self.html_templates.option_base.format(
                endonym=endonym,
                language_name=language_name,
                selected="selected " if current_language is "en" else "",
                language_code=current_language,
                xlet_help=xlet_help,
                xlet_contributors=xlet_contributors,
                xlet_changelog=xlet_changelog,
                title=title
            )
        else:
            return None

    def get_introduction(self):
        return self.html_templates.introduction_base.format(
            # TO TRANSLATORS: Full sentence:
            # "Help for <xlet_name>"
            md("# %s" % (_("Help for %s") % xlet_meta["name"])),
            md("## %s" % _("IMPORTANT!!!")),
            md(_("Never delete any of the files found inside this xlet folder. It might break this xlet functionality.")),
            md(_("Bug reports, feature requests and contributions should be done on this xlet's repository linked next.") +
               " %s" % ("[GitHub](%s)" % xlet_meta["website"] if xlet_meta["website"] else xlet_meta["url"]))
        )

    def get_localize_info(self):
        return md("\n".join([
            "## %s" % _("Applets/Desklets/Extensions (a.k.a. xlets) localization"),
            "- %s" % _("If this xlet was installed from Cinnamon Settings, all of this xlet's localizations were automatically installed."),
            # TO TRANSLATORS: MARKDOWN string. Respect formatting.
            "- %s" % _("If this xlet was installed manually and not trough Cinnamon Settings, localizations can be installed by executing the script called **localizations.sh** from a terminal opened inside the xlet's folder."),
            "- %s" % _("If this xlet has no locale available for your language, you could create it by following the following instructions.") +
            " %s" % "[Wiki](https://github.com/Odyseus/CinnamonTools/wiki/Xlet-localization)"
        ]))


if __name__ == "__main__":
    parser = ArgumentParser(usage=localized_help_modules.USAGE)
    group = parser.add_mutually_exclusive_group(required=False)

    group.add_argument("-p",
                       "--production",
                       help="Creates the help file into a temporary folder.",
                       action="store_true",
                       dest="production",
                       default=False)
    group.add_argument("-d",
                       "--dev",
                       help="Creates the help file into its final destination.",
                       action="store_true",
                       dest="dev",
                       default=False)

    options = parser.parse_args()

    if not (options.production or options.dev):
        parser.print_help()
        quit()

    help_file_path = None
    creation_type = None

    if options.production:
        creation_type = "production"
        help_file_path = os.path.join(XLET_DIR, "files", XLET_UUID, "HELP.html")
    elif options.dev:
        creation_type = "dev"
        repo_tmp_folder = os.path.join(repo_folder, "tmp", "help_files")
        GLib.mkdir_with_parents(repo_tmp_folder, 0o755)
        help_file_path = os.path.join(repo_tmp_folder, XLET_UUID + "-HELP.html")

    if help_file_path is not None:
        m = Main()
        m.creation_type = creation_type
        m.help_file_path = help_file_path
        m.do_dummy_install()
