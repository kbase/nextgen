/*
 * The Invocation Service provides a mechanism by which KBase clients may
 * invoke command-line programs hosted on the KBase infrastructure. 
 * 
 * The service provides a simple directory structure for storage of intermediate
 * files, and exposes a limited set of shell command functionality.
 */
module InvocationService
{
    /*
     * A directory entry. Used as the return from list_files.
     */
    typedef structure {
	string name;
	string full_path;
	string mod_date;
    } directory;

    /*
     * A file entry. Used as the return from list_files.
     */
    typedef structure {
	string name;
	string full_path;
	string mod_date;
	string size;
    } file;

    authentication optional;
    
    /* 
     * Begin a new session. A session_id is an uninterpreted string that
     * identifies a workspace with in the Invocation Service, and serves to
     * scope the data stored in that workspace.
     *
     * If start_session is invoked with valid authentication (via the standard
     * KBase authentication mechanisms), the session_id is ignored, and an
     * empty session_id returned. Throughout this service interface, if
     * any call is made using authentication the given session_id will be ignored.
     */
    funcdef start_session(string session_id) returns (string actual_session_id);

    /*
     * Enumerate the files in the session, assuming the current working
     * directory is cwd, and the filename to be listed is d. Think of this
     * as the equivalent of "cd $cwd; ls $d".
     */
    funcdef list_files(string session_id, string cwd, string d) returns (list<directory>, list<file>);

    /*
     * Remove the given file from the given directory.
     */
    funcdef remove_files(string session_id, string cwd, string filename) returns ();

    /*
     * Rename the given file.
     */
    funcdef rename_file(string session_id, string cwd, string from, string to) returns ();

    /*
     * Copy the given file to the given destination.
     */
    funcdef copy(string session_id, string cwd, string from, string to) returns ();

    /*
     * Create a new directory.
     */
    funcdef make_directory(string session_id, string cwd, string directory) returns ();

    /*
     * Remove a directory.
     */
    funcdef remove_directory(string session_id, string cwd, string directory) returns ();

    /*
     * Change to the given directory. Returns the new cwd.
     */
    funcdef change_directory(string session_id, string cwd, string directory) returns (string);

    /*
     * Write contents to the given file.
     */
    funcdef put_file(string session_id, string filename, string contents, string cwd) returns ();

    /*
     * Retrieve the contents of the given file.
     */
    funcdef get_file(string session_id, string filename, string cwd) returns (string contents);

    /*
     * Run the given command pipeline. Returns the stdout and stderr for the pipeline.
     *
     * If max_output_size is greater than zero, limits the output of the command
     * to max_output_size lines.
     */
    funcdef run_pipeline(string session_id, string pipeline, list<string> input, int max_output_size, string cwd)
	returns (list<string> output, list<string> errors);

    /*
     * Experimental routine.
     */
    funcdef run_pipeline2(string session_id, string pipeline, list<string> input, int max_output_size, string cwd)
	returns (list<string> output, list<string> errors, string stdweb);

    /*
     * Exit the session.
     */
    funcdef exit_session(string session_id) returns ();

    /*
     * Description of a command. Contains the command name and a link to documentation.
     */
    typedef structure {
	string cmd;
	string link;
    } command_desc;

    /*
     * Description of a command group, a set of common commands.
     */
    typedef structure {
	string name;
	string title;
	list<command_desc> items;
    } command_group_desc;

    /*
     * Retrieve the set of valid commands.
     *
     * Note that this does not require authentication or a valid session, and thus
     * may be used to set up a graphical interface before a login is done.
     */
    funcdef valid_commands() returns (list<command_group_desc>);

    /*
     * Retrieve the set of modules installed in the current deployment.
     *
     * Note that this does not require authentication or a valid session, and thus
     * may be used to set up a graphical interface before a login is done.
     */
    funcdef installed_modules() returns (list<string>);

    /*
     * Retrieve the tutorial text for the given tutorial step, along with the
     * the step numbers for the previous and next steps in the tutorial.
     */
    funcdef get_tutorial_text(int step) returns(string text, int prev, int next);
};
