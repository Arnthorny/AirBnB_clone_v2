#!/usr/bin/python3
"""
This program contains the entry point of
the command interpreter (console).
"""
import cmd
import sys
from models import storage
from models import MODELS
import re
import json
import shlex


regex_line = r"^(?:(?P<class>\S+)\.(?P<cmd>\S+)\((?P<args>.*)\))$"
regex_id_dict = r'^(?:(?P<id>".*?"), (?P<dct>\{.*?\}))$'
regex_id_attr_val = (r'^(?:(?:(?P<id>".*?"),) (?:(?P<attr>".*?"),) '
                     r'(?P<val>"[^"]*?"|\d+\.\d+|\d+))$')
# regex_id_attr = r'^(?:["\'](?P<id>\S+)["\'], ["\'](?P<attr>\S+)["\'])$'
regex_id_attr = r'^(?:(?:(?P<id>".*?"),) (?P<attr>".*?"))$'
# regex_id = r'^(?:["\'](?P<id>\S+?)["\'])$'
regex_id = r'^(?P<id>".*?")$'


def split_l(line):
    """
    This function splits a line with a syntax resembling
    that of the Unix shell using the ``shlex`` module.

    The split function of the `shlex` module is used here but re is faster.

    Args:
        line(str): Line to be split.
    Returns:
        (list): List of tokens split from line
    """
    # return re.findall(r'[^"\s]\S*|["\'].+?["\']', line)
    return shlex.split(line)


class HBNBCommand(cmd.Cmd):
    """
    This class will be used to define functions implemented in
    the command interpreter
    """

    prompt = "(hbnb) "

    def emptyline(self):
        """This line overwrites the `emptyline + ENTER` default command"""
        pass

    def do_quit(self, arg):
        """Quit command to exit the program
        """
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program
        """
        print()
        return True

    def handle_update(self, match, line):
        """
        This function handles an update command
        when passed in the methodlike form.

        Args:
            match(`obj`:re): This re object holds the initial line match groups
            line(str): Line of input
        """
        id_args_or_id_dict = match.group('args')
        match_dict = re.search(regex_id_dict, id_args_or_id_dict)
        match_id_attr_val = re.search(regex_id_attr_val, id_args_or_id_dict)
        match_id_attr = re.search(regex_id_attr, id_args_or_id_dict)
        match_id = re.search(regex_id, id_args_or_id_dict)

        if match_dict:
            dict_str = match_dict.group('dct').replace('\'', '"')
            dct_object = json.loads(dict_str)
            dct_it = list(dct_object.items())
            if len(dct_it) == 0:
                return ''
            for i in range(len(dct_it)):
                new_line = (f"{match.group('cmd')} {match.group('class')} "
                            f"{match_dict.group('id')} {dct_it[i][0]} "
                            f'"{dct_it[i][1]}"')
                if len(dct_it) == 1 or i == len(dct_it) - 1:
                    return new_line
                else:
                    ret_val = self.onecmd(new_line)
                    if ret_val is False:
                        return ''
        elif match_id_attr_val:
            new_line = (f"{match.group('cmd')} {match.group('class')} "
                        f"{match_id_attr_val.group('id')} "
                        f"{match_id_attr_val.group('attr')} "
                        f'"{match_id_attr_val.group("val")}"')
            return new_line
        elif match_id_attr:
            new_line = (f"{match.group('cmd')} {match.group('class')} "
                        f"{match_id_attr.group('id')} "
                        f"{match_id_attr.group('attr')}")
            return new_line
        elif match_id:
            new_line = (f"{match.group('cmd')} {match.group('class')} "
                        f"{match_id.group('id')}")
            return new_line
        elif match.group('args').strip() == '':
            new_line = "{} {} {}".format(match.group('cmd'),
                                         match.group('class'),
                                         match.group('args'))
            return new_line
        else:
            return line

    def parseline(self, line):
        """Parse the line into a command name and a string containing
        the arguments.  Returns a tuple containing (command, args, line).
        'command' and 'args' may be None if the line couldn't be parsed.

        Args:
            line(str): Line of input
        Returns:
            (str)
        """
        match = re.search(regex_line, line)
        if match:
            m_args = match.group('args')
            m_args_is_blank = m_args == ''
            m_args_maybe_id = re.fullmatch('^["\'].*["\']$', m_args)
        if match is None:
            return cmd.Cmd.parseline(self, line)
        elif match.group('cmd') == 'update':
            return (cmd.Cmd.parseline(self, self.handle_update(match, line)))
        elif (match.group('cmd') in ['all', 'count']
                and not m_args_is_blank):
            # Invalid Syntax
            return cmd.Cmd.parseline(self, line)
        elif (match.group('cmd') in ['destroy', 'show']
                and m_args_maybe_id is None):
            return cmd.Cmd.parseline(self, line)
        else:
            new_line = "{} {} {}".format(match.group('cmd'),
                                         match.group('class'),
                                         match.group('args'))
            return cmd.Cmd.parseline(self, new_line)

    @staticmethod
    def initial_checks(arg_l, count=3):
        """This function performs error checks that common to some
        interpreter commands.

        Args:
            arg_l(list): Given argument to perform error checks on
            count(int): Number of checks to perform for given call

        Returns:
            (bool): True if an error occured else False
        """
        if not arg_l:
            print("** class name missing **")
        elif count >= 2 and arg_l[0] not in MODELS:
            print("** class doesn't exist **")
        elif count >= 3 and len(arg_l) == 1:
            print("** instance id missing **")
        else:
            return False
        return True

    @staticmethod
    def extract_args(arg_l):
        """This function extracts keyword arguments from a list
        of strings.

        Args:
            arg_l(list): List of strings in the form: `<key name>=<value>`

        Returns:
            (dict): Dictionary containing valid parameters
        """
        new_dict = {}

        for arg in arg_l:
            p_arg = arg.partition('=')
            if not p_arg[1]:
                continue

            key = p_arg[0]
            val = p_arg[2]
            new_val = None

            if val[0] == '"' and val[-1] == '"':
                new_val = val.replace('_', ' ').strip('"')
            else:
                try:
                    val_num = float(val)
                    new_val = int(val_num) if '.' not in val else val_num
                except (ValueError, TypeError):
                    pass
            if new_val:
                new_dict[key] = new_val
        return new_dict

    def do_create(self, arg):
        """Creates a new instance of a Model,
        saves it (to the JSON file) and prints the id.
        Ex: $ create BaseModel
            $ create <Class name> <param 1> <param 2> <param 3>
            Param syntax: <key name>=<value>
        """
        arg_l = split_l(arg)
        if self.initial_checks(arg_l, 2):
            pass
        else:
            instance = None
            if len(arg_l) > 1:
                args_dict = self.extract_args(arg_l[1:])
                instance = MODELS[arg_l[0]](**args_dict)
            else:
                instance = MODELS[arg_l[0]]()
            instance.save()
            print(instance.id)

    def do_show(self, arg):
        """Prints the string representation of an instance,
        based on the class name and id.
        Ex: $ show BaseModel 1234-1234-1234
        """
        arg_l = split_l(arg)
        arg_l = [x.strip('"\'') for x in arg_l]
        if self.initial_checks(arg_l):
            pass
        else:
            key = f"{arg_l[0]}.{arg_l[1]}"
            o = storage.all().get(key)
            print(o if o else "** no instance found **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id and
        saves the change into the JSON file.
        Ex: $ destroy BaseModel 1234-1234-1234.
        """
        arg_l = split_l(arg)
        arg_l = [x.strip('"\'') for x in arg_l]
        if self.initial_checks(arg_l):
            pass
        else:
            key = f"{arg_l[0]}.{arg_l[1]}"
            obj = storage.all().pop(key, None)
            if obj:
                storage.delete(obj)
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """Prints all string representation of all instances
        based or not on the class name.
        Ex: $ all BaseModel or $ all or $ <class name>.all().
        """
        arg_l = split_l(arg)
        arg_l = [x.strip('"\'') for x in arg_l]
        if len(arg_l) >= 1 and arg_l[0] not in MODELS:
            print("** class doesn't exist **")
        else:
            if not arg_l:
                all_o = [o for o in storage.all().values()]
            else:
                all_o = [o for o in storage.all().values()
                         if type(o).__name__ == arg_l[0]]
            all_inst = [str(x) for x in all_o]
            all_inst.reverse()
            print(all_inst)

    def do_count(self, arg):
        """Counts all instances based on the class name.
        Ex: $ count BaseModel or $ <class name>.count()
        """
        arg_l = split_l(arg)
        arg_l = [x.strip('"\'') for x in arg_l]
        if arg_l[0] not in MODELS:
            print("** class doesn't exist **")
        else:
            all_o = [o for o in storage.all().values()
                     if type(o).__name__ == arg_l[0]]
            print(len(all_o))

    def do_update(self, arg):
        """Update an instance based on the class name and id by adding/updating
        attribute and save the change into the JSON file).
        Ex: $ update BaseModel 1234-1234-1234 email "aibnb@mail.com"
        Returns:
            None to indicate success or 1 to indicate error
        """
        arg_l = split_l(arg)
        arg_l = [x.strip('"\'') for x in arg_l]
        if self.initial_checks(arg_l):
            pass
        elif not (o := storage.all().get(f"{arg_l[0]}.{arg_l[1]}")):
            print("** no instance found **")
        elif len(arg_l) == 2:
            print("** attribute name missing **")
        elif len(arg_l) == 3:
            print("** value missing **")
        else:
            val = arg_l[3]
            if not hasattr(o, arg_l[2]):
                val_type = str
            else:
                val_type = type(getattr(o, arg_l[2]))
            val = val_type(val) if val_type != int else int(float(val))
            """
            try:
                val_num = float(val)
                val = int(val_num) if '.' not in val else val_num
            except (ValueError, TypeError):
                pass
            """
            setattr(o, arg_l[2], val)
            o.save()
            return None
        return False


if __name__ == '__main__':
    HBNBCommand().cmdloop()
