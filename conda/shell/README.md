# Flowchart of Activation Process

```mermaid
%%{init: {"flowchart": {"htmlLabels": false}} }%%
flowchart TD
	start1(["`run **conda shell.bash activate** using the CLI`"])
	start2(["`run **python -m conda shell.bash activate** using the CLI`"])
	start3(["`run **conda activate** using the CLI`"])
	
	s2i["`**__main__.py**: call **main** function in conda executable`"]
	m1["`**main**: parse CLI input`"]
	
	m1.D{"`CLI input contains **shell.** in first argument?`"}
	m1.D1(["`**main_subshell**: handle subshell subcommands (e.g., conda create)`"])
	m2["`**main_sourced**: call _build_activator_cls function for specified shell`"]
	
	m2.D{"`**_build_activator_cls**: specified shell string \n in activator_map dictionary?`"}
	m2.D1(["`raise error: shell is not a supported shell`"])
	m3["`**_build_activator_cls**: return type object containing relevant activator class`"]

	m4["`**main_sourced**: initialize **context**`"]

	m5["`create a class instance of the relevant activator class (in this case, PosixActivator). \n Through this process, the necessary facets of the relevant shell scripting language are declared for later use.`"]

	m6["`call *_Activator's* **execute** method and print the result to the terminal. \n End with an empty string rather than with a new line.`"]

	m7["`**_Activator.execute**: calls *_Activator's* **_parse_and_set_args** method with any CLI arguments passed into the class at initialization)`"]
	
	m7.D{"`**_Activator._parse_and_set_args**: \n Is the arguments list missing or empty?`"}
	m7.D1["`Raise error and send a warning / informational message to the command line, using \n the **raise_invalid_command_error** helper function`"]

	m8i["`Separate *command* (first CLI argument in argument list) from remaining arguments`"]
	m8ii["`Determine if there are help flags in the argument list`"]
	
	m8.Di{"`Is the first argument in the \n arguments list an empty string?`"}
	
	m8.Dii{"`Are there help flags in \n the arguments list?`"}
	m8.Dii.1["`Bring up the appropriate help message`"]
	
	m8.Diii{"`Is *command* NOT a conda \n shell command ('activate', 'deactivate', \n 'hook', 'commands', or 'reactivate')?`"}

	m8.Div{"`Does *command* end with 'activate' or is **command** 'hook'?`"}

	m9["`Check for the '--dev' flag in the list of remaining arguments`"]
	
	m9.D{"`Is the '--dev' flag in the list of remaining arguments?`"}
	m9.D1["`Set *context.dev* to *False*`"]
	m9.D2["`Delete the '--dev' flag from the list \n of arguments and set *context.dev* to *True*`"]
	
	m8.Dv{"`Is *command* 'activate'?`"}
	m8.Dv.1["`Set *self.stack* to *context.auto_stack* \n only if *context.shlvl* <= *context.auto_stack*`"]
	
	m10["`Set *stack_idx* to the argument list index number \n that contains the '--stack' flag if the flag \n is in the argument list and to \n -1 if the flag is not in the argument list `"]
	m11["`Set *no_stack_idx* to the argument list index number \n that contains the '--no-stack' flag if the flag \n is in the argument list and to \n -1 if the flag is not in the argument list`"]
	
	m11.Di{"`Are both the '--stack' flag and \n the '--no-stack' flag \n in the argument list?`"}
	m11.Di.1["`Raise error and send message to the command line"]

	m11.Dii{"`Is the '--stack' flag \n in the argument list?`"}
	m11.Dii.1["`Set *self.stack* to *True* and delete the '--stack' flag from the argument list`"]

	m11.Diii{"`Is the '--no-stack' flag \n in the argument list?`"}
	m11.Diii.1["`Set *self.stack* to *False* and delete the '--no-stack' flag from the argument list`"]

	m11.Div{"`Are there remaining arguments \n in the argument list?`"}
	m11.Div.1["`Raise error and send message to the command line"]

	m12["`Set *self.command* to *command*`"]

	m13["`**_Activator.execute**: return *self.command*`"]
	
	m14["`**main_sourced**: print *self.command* to the terminal `"]

	End1(["`return successful exit code or handle errors that have occurred during the process`"])


	start2 --> s2i
	s2i --> m1
	start1 --> m1
	
	m1 --> m1.D
	m1.D -. no .-> m1.D1
	m1.D -- "yes: 'shell.bash'" --> m2

	m2 --> m2.D
	m2.D -. no .-> m2.D1
	m2.D -- "yes: 'bash'" --> m3

	m3 --> m4
	m4 --> m5
	m5 --> m6
	m6 --> m7

	subgraph a [activate.py]
	m7 --> m7.D

	subgraph b [_Activator._parse_and_set_args]
	m7.D -. yes .-> m7.D1
	m7.D -- no --> m8i

	m8i --> m8ii
	m8ii --> m8.Di

	m8.Di -. yes .-> m7.D1
	m8.Di -- "no: 'activate'" --> m8.Dii
	
	m8.Dii -. yes .-> m8.Dii.1
	m8.Dii -- no --> m8.Diii

	m8.Diii -. yes .-> m7.D1
	m8.Diii -- "no: 'activate'" --> m8.Div

	m8.Div -. yes .-> m9
	m8.Div -- no --> m8.Dv
	
	m9 -.-> m9.D
	
	m9.D -. no .-> m9.D1
	m9.D -. yes .-> m9.D2
	m9.D1 -.-> m8.Dv
	m9.D2 -.-> m8.Dv

	m8.Dv -- yes --> m8.Dv.1
	m8.Dv.1 --> m10
	m10 --> m11

	m11 --> m11.Di
	
	m11.Di -- no --> m11.Dii
	m11.Di -. yes .-> m11.Di.1
	m11.Di.1 -.-> m11.Dii

	m11.Dii -- no --> m11.Diii
	m11.Dii -. yes .-> m11.Dii.1
	m11.Dii.1 -.-> m11.Diii

	m11.Diii -- no --> m11.Div
	m11.Diii -. yes .-> m11.Diii.1
	m11.Diii.1 -.-> m11.Div

	m11.Div -- no --> m12
	m11.Div -. yes .-> m11.Div.1
	end

	m12	--> m13
	end

	m13 --> m14

	m14 --> End1
```