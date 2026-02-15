# PG 2.20 to 2.16 features

## WeBWorK 2.20

Source: [https://wiki.openwebwork.org/wiki/Release_notes_for_WeBWorK_2.20](https://wiki.openwebwork.org/wiki/Release_notes_for_WeBWorK_2.20)


### New WeBWorK 2.20 Features


- Fix several security vulnerabilities [1], [2], [3], [4], [5]
- Improvements to efficiency of database calls ([6], [7], [8], [9], [10], [11], [12])
- Fix a memory leak, which should improve memory usage by WeBWorK processes [13]
- Change student and instructor emails from plain text to HTML [14]
- Allow the ability to synchronize section information from your Learning Management System when using LTI authentication [15]
- You can now load a problem directly from the Problem Editor, or start with any of the sample problems [16]
- Students can now use achievement items directly from the Problem Set page [17]
- The "Upgrade Courses" feature in Course Administration now checks and fixes additional things:
- Data types of database columns are checked and corrected [18]
- Links to standard libraries and problems (Open Problem Library, Contrib, Student Orientation) are added if they are not present. [19]
- There are now more options for adding users during new course creation (e.g. adding multiple instructors during course creation) [20]
- Add the ability to manage secrets for two-factor authentication to the admin interface [21]
- More configurability for when grades are sent back to the Learning Management System using LTI [22]
- Update the Shibboleth authentication module to work with the current version of WeBWorK [23]
- Fix error in displaying how often grades are sent back to the LMS [24]
- Problem editor upgraded to CodeMirror 6, introduces new features: accordioning, autocompletion, improved syntax highlighting [25]
- Add option for LTI 1.3 where students can work on assignments even if they are not linked to the LMS and grade passback is set to homework [26]
- Importing set definition files with paths to problem files that contain spaces now works [27]

### New PG 2.20 Features and Improvements


- Improvements to degree n matrices (matrices/tensors of more than two dimensions) [28]
- The interface with Rserve has been rewritten within PG. The `Statistics::R::IO::Rserve` package is no longer required or used [29]
- Improvements to the GraphTool [30]
- Tools for polygons [31]
- Sine wave tool added [32]
- Vector tool added [33]
- Improvements to fill tool [34]
- Improvements to contextReaction.pl [35]
- New contextExtensions.pl [36]
- Fraction contexts are now extensions of the parent context [37]
- Units now implemented as MathObject classes, contextUnits.pl [38]
- New plots.pl macro that allows a more modern, more efficient way of generating a wide variety of plots. See documentation at https://webwork.maa.org/pod/pg/macros/graph/plots.html [39]
- Ability to use full html in drop-down menu items [40]

### Breaking changes


- custom_problem_grader_0_60_100 has been removed. Problems should be converted to custom_problem_fluid
- Change in behaviour when comparing a degree 1 matrix and a degree 2 matrix [41]

### Updated Dependencies

- It is recommended to install Cpanel::JSON::XS
- Any version of perltidy
- Several perl packages are no longer required, and can be removed from your system
- Array::Utils
- Email::Sender::Simple
- HTML::Tagset
- HTML::Template
- IO::Socket::SSL
- JSON
- JSON::MaybeXS
- Net::LDAPS
- Net::SMTP
- Net::SSLeay
- Padwalker
- Path::Class
- Safe
- Statistics::R::IO
- Template



## WeBWorK 2.19

Source: [https://wiki.openwebwork.org/wiki/Release_notes_for_WeBWorK_2.19](https://wiki.openwebwork.org/wiki/Release_notes_for_WeBWorK_2.19)


### New WeBWorK 2.19 Features


- The attempts table has been removed. Feedback for correct/incorrect answers is now associated directly with each answer blank.
- The PG editor now has an option to convert problems to PGML although conversion is not complete and needs further editing to get a functional problem. So use with care.
- The problem sets page has been reworked. The order that sets are presented to students has been made more intuitive, and can be sorted by the student.
- The "Hmwk Sets Editor" has been renamed to "Sets Manager", and the "Classlist Editor" is now called "Accounts Manager".
- In the "Accounts Manager" all user aspects (including password and permission level) can now be set when a user is first created, and all user aspects can now be edited at once on the edit tab (there is not a separate password tab anymore).
- The "Report bugs" link now points to GitHub issues rather than bugzilla.
- The file manager has been updated with the following feaures:
- Archiving and unarchiving now supports the .zip archive format.
- Clicking on the edit link for a problem file (.pg) now opens that file in the problem editor.
- The course.conf and simple.conf files are now truly not editable by users that do not have admin permissions.
- The "Instructor Tools" page has been redesigned.
- There are new sort options on users and sets.
- The user interface has been improved.
- The PGML lab problem has been redesigned.
- All of the examples have been updated.
- Now there are examples that include all PGML features.
- The problem is now hosted on the local webwork server instead of the defunct Rochester webwork server, and so will always work.
- Two-factor authentication using an authenticator app is now available, and is enabled by default (see the Two Factor Authentication section of `defaults.config`.
- The course that is used for Course Administration can now be customized. It is recommended that you change from the previously hard coded "admin" course to something of your choosing. Having the name of the admin course be publicly known is a security vulnerability.
- Changing tabs on the instructor course configuration page doesn't reload the page, and when the course configuration is saved the new settings take effect immediately without another page reload.
### Achievement changes

- The following achievement items can now be applied to sets for which the due date has passed: Cupcake of Enlargement, Cake of Enlargement, Greater Rod of Revelation, Greater Tome of Enlightenment, Lesser Rod of Revelation, Lesser Tome of Enlightenment.
- A new achievement item has been added to provide students with a set of assignment extensions that they can apply on their own. Simply import the `extensions.at` achievement.
- WeBWorK now supports authentication for SMTP servers. See site.conf.dist and localOverrides.conf.dist for details.
- The `$sessionKeyTimeout` configuration variable has been replaced with `$sessionTimeout`, and applies more generally to session cookies.
- A new student orientation set has been created, and separated from the Model course. These problems now refer to the current version of WeBWorK.
- Proctor authentication fix (#2347)
- When using LTI 1.3 you can now separately set the Access Token Audience ($LTI{v1p3}{AccessTokenAUD}) and Access Token URL ($LTI{v1p3}{AccessTokenURL}).
- A content selection tool is available when using LTI, which if enabled by your learning management system administrator will allow instructors to select an assignment or a course to link in the LMS. See LTI_Authentication_(for_WeBWorK_2.18_or_newer)#Setup_Courses_To_Use_Content_Selection.
- Certbot renewal routes (#2321)
- Added the ability to filter student progress on a single set by section/recitation ([#2320])
- If reduced scoring is enabled, then student progress shows a question as complete if the student has achieved the highest possible score [#2301].
- When creating a new course you can now copy more things from an existing course (templates and html folders, simple configuration file, non-student users, assignments/sets, achievements, course title, course institution)
- You are now given the ability to upgrade a course while unarchiving.

### New PG 2.19 Features and Improvements


### New PGML features

- Tables, PGML A new syntax is added to create tables within PGML blocks using niceTables.pl. Also, the niceTables.pl macro is automatically loaded when using PGML.
- Tags, PGML One can now add HTML div or span tags within PGML with [< ... >].
- The contextBoolean.pl macro was added with a Boolean MathObject context which includes:
- parsing of boolean expressions,
- reduction rules with and's and or's
- customizable true and false symbols and provision of unicode versions.
- Additional methods were added to Matrix MathObjects including:
- the ability to create zero, permutation and elementary matrices
- test for triangular, orthogonal, diagonal, symmetric matrices
- test if matrices are in row echelon or reduced row-echelon forms.
- A general macro parserMultipleChoice.pl was added that loads all the multiple choice parsers: PopUp, CheckboxList, RadioButtons, RadioMultiAnswer
- Updated and fixed PGML horizontal rules. Rules, PGML
- The methods num and den have been added to fraction MathObjects (those created in the contexts provided by the contextFraction.pl macro).
- Change the behavior of Compute. If Compute is called on a number, then a Real will now be created on that number. Before it was stringified and passed to Formula.
- Knowls have been reworked (again). Knowl links no longer attempt to open directly in the page. Instead they open in a modal dialog.
- There have been many accessibility improvements.

### Breaking changes


- parserPopUp.pl has changed the default handling when the correct answer is defined to be a non-negative integer. That will now be treated as an index into the array of answers (to be consistent with other macros) and not as the "answer" from the array. See: PR#1019. Some sites may want to temporarily change the default back to the old behavior, and maybe use a modified version of the file on their servers to locate problems which may not behave as intended after the change. See Issue#1139.

### Deprecated Functionality


- All versions of the compound problem macro have been deprecated (compoundProblem.pl, compoundProblem2.pl, and compoundProblem5.pl). Problems should be migrated to use the scaffold.pl macro.




## WeBWorK 2.18

Source: [https://wiki.openwebwork.org/wiki/Release_notes_for_WeBWorK_2.18](https://wiki.openwebwork.org/wiki/Release_notes_for_WeBWorK_2.18)


### New WeBWorK 2.18 Features


### UI Changes for WeBWorK

- The overall layout of WeBWorK has changed a bit with the sidebar navigation menu scrolling independently of the main content.
- The page Help (which was a ? icon in the navigation list) has been moved to a ? next to the page title. The page help for each page has been improved.
- The instructor Tools is more clearly a separate page rather than a Header for other tools.
- The Set Assigner and Problem Editor can now be directly accessed from the sidebar navigation.
- The Student Progress page has a new option to show 'Time remaining' for tests.
- The Stats page has been rewritten for layout and clarity.
### PG problem editor improvements

- The layout of the page is updated to include a source editor and viewer in a side-by-side manner.
- There is a new Generate Hardcopy tab from which you can generate a PDF displaying only the problem being edited. This makes it much easier to test hardcopy generation for problems.
- There are new problem viewing output formats (TeX and PTX -- PreTeXt).
- The Update/New Version tab options are now called Save/Save As...
- There are options to save backups for pg problems. (documentation?)
- The date/time widget (flatpicker) now includes a "Now" and "Today" button to set the date/time to now or adjust the date only respectively.
- A new LTI version 1.3 authentication module has been added that utilizes some of the LTI Advantage tool set. The LTI version 1.1 authentication module is still available.
- A new status called "observer" has been added. This can be used for TAs and professors or others to ensure that they don't show up in scoring, statistics and student progress views. They will be shown in green in the Classlist Editor.
- Gateway quizzes are now called Tests.
- Hardcopy generation has been revamped. A new hardcopy theme system has been devised. Each theme is contained in a single XML file. These theme files can be edited from the PG problem editor. There are eleven themes distributed with webwork2. See Hardcopy Themes.
- The ability to save/retrieve data within pg problems on a user-set level has been added. (Needs documentation)
- Essay answers
- There is now an equation editor to insert math via MathQuill (similar in nature to the MathView equation editor).
- This equation editor is also available for manual graders.
- When using the problem grader, there is now an option for using points (default), percent or both. This is a new option in the Problem Display/Answer Checking tab of the Course Configuration.
- The Wiris Math Editor has been removed. It was never functional and input is better handled by MathQuill.

### New PG 2.18 Features


### Built-in Features

- Images can be inserted in PGML with the code [!alt text!]{image source}{optional width}{optional height}. See the wiki page on PGML images and a sample problem.

### New PG 2.18 Macros

- There is a new macro for plotting three dimensional curves and surfaces using the plotly.js JavaScript library. See the POD for plotly3D.pl and sample problems on space curves and surface graphs.
- A new macro allows you to generate a random name for a person. Methods are provided to insert the correct pronouns (he, she, or they) for that name into sentences. See the POD for randomPerson.pl and a sample problem.
- There is a new MathObject checkboxes macro for creating multiple choice checkbox answers. See the POD for parserCheckBoxList.pl and a sample problem.
- A new macro allows authors to tie a radio answer together with several answer blanks that are dependent on the radio choice. See the POD for parserRadioMultiAnswer.pl and a sample problem.
- There is a new linear relation context for lines and linear inequalities. See the POD for parserLinearRelation.pl and a sample problem.
- A new specialTrigValues.pl macro provides the standard values of trig functions on the unit circle. See the POD for specialTrigValues.pl and a sample problem.

### Updates to existing PG 2.18 macros

- The niceTables.pl macro has been completely overhauled. See the POD for niceTables.pl and a sample problem.
- Authors can now specify values for checkbox and radio answers added via the parserCheckboxList.pl and parserRadioButtons.pl macros that will be displayed on the past answers page (instead of B0, B1, etc., as was previously shown). See the POD for parserCheckboxList.pl and POD for parserRadioButtons.pl.
- The graphTool macro has been updated:
- There is now a number line mode for graphing intervals.
- There are default answer checkers that make writing graph tool problems easier.
- A generateAnswerGraph method has been added which shows the correct answer graph. This is useful for solutions.
- A dynamic help system has been implemented to help students use the graph tool.
- See the following sample problems: Number Line Mode, Plotting a Circle, Plotting a Cubic, Plotting a Line, Plotting Points
- Also see the POD for parserGraphTool.pl.
- There is a new DropDown method provided by the parserPopup.pl macro. See the POD for parserPopUp.pl and a sample problem.

### Mathquill changes

- Typing `deg` will automatically turn into a degree symbol. So for example, if `23degF` is typed it will render with a degree symbol.
- Trigonometric functions such as sin, cos, tan, arcsin, arccos, etc, and logarithmic functions ln and log will now automatically wrap the function argument in parentheses. Exponents (or subscripts) on these functions can be typed before the parentheses or after.
- Double and triple click selection behavior has been implemented for MathQuill inputs.

### Changes to Units

- Students can enter degree-symbol Celsius/Fahrenheit forms instead of `degC` or `degF` for Celsius and Fahrenheit degrees. This can be done easily if MathQuill is enabled as described above. Students may also paste Unicode characters for these from other websites.
- Several new units have been added, including angstroms, microseconds, nanoseconds, picometers, femtometers, tera electron volts, Megawatts, milliwatts, milliCoulombs, microCoulombs, nanoCoulombs, milli-amperes, milli-teslas, Becquerels, (US) gallons, (US) quarts, and (US) pints.
- Many unicode characters for units have been added.
- More forms of units are now allowed including plural forms. For example, one may enter 30 ft, 30 feet, or 1 foot.

### Deprecated PG 2.18


### Deprecated PG 2.18 Macros

- AnswerFormatHelp.pl: Authors should now use the helpLink function from PGbasicmacros.pl instead.
- unionInclude.pl: This was used for random problems.
- Although not officially deprecated at this point, unionTables.pl should not be used due to accessibility and html validation issues. Use niceTables.pl instead.

### Other PG 2.18 Deprecation

- `$BEGIN_ONE_COLUMN` and `$END_ONE_COLUMN`: These have often been used in set header files. These variables are now defined to be the empty string, and no longer actually start or end one column mode. Set headers are now always inserted in one column mode in hardcopy.

### Security/Advanced Features


- The backend of WeBWorK has been relying on mod_perl for nearly two decades. However, mod_perl is deprecated and has not been updated since 2011. Many Linux distributions no longer support mod_perl, and it is becoming increasing difficult to install it on some of them. The server part of WeBWorK is now implemented with Mojolicious, which includes a stand alone web server (hypnotoad) written completely in Perl.




## WeBWorK 2.17

Source: [https://wiki.openwebwork.org/wiki/Release_notes_for_WeBWorK_2.17](https://wiki.openwebwork.org/wiki/Release_notes_for_WeBWorK_2.17)


### New WeBWorK 2.17 Features


- As with WeBWorK 2.16, third party javascript libraries (jquery, jquery-ui, mathjax, codemirror, etc.) are installed via npm. WeBWorK 2.17 does even more. Now WeBWorK's own javascript and css files are minimized, and generated with a filename containing a hash of its contents. This means that users will not need to clear their browser cache when WeBWorK is upgraded. In addition if you would like to serve third party javascript from a remote CDN instead of serving these files from your server, there is an installation option to set that up.
- Students may now attach files to emails they send to instructors via the "Email Instructor" page.
- The look and feel of the user interface of WeBWorK is quite different, mainly because Bootstrap has been updated from version 2.3.2 to version 5.1.3. This gives a much more modern feel.
- The theming of WeBWorK has changed significantly. Themes written for previous versions of WeBWorK will no longer work. See Customizing WeBWorK for information on how to create new themes.
- Instructors may now create sets with spaces in the name. Technically the spaces are translated into underscores and the set names are stored that way, but anytime a set name appears in the user interface it will be shown with spaces.
- It is now possible to delete a specific version of a Gateway quiz for a student. This can be done on the page opened when you click on the "Assigned Sets" column for a user in the Classlist Editor.
- When a student clicks "Grade Test" in a gateway quiz, a confirmation dialog will open that informs the student of the consequences of submitting the quiz and gives the student a chance to decline submission.
- Gateway quiz versions are no longer listed on the course homepage (the Homework Sets page). Instead they are listed on a page that opens when you click on the Gateway quiz template. This page also gives the student more details on the Gateway quiz and displays a set info much like the problem list page for regular homework sets. If you are using LTI authentication and provide direct links to homework assignments or quizzes, then it is recommended that you now direct the students to this page for Gateway quizzes rather than directly into the the quiz. So use a link that looks something like "https://yourserver.edu/webwork2/courseID/setID" instead of "https://yourserver.edu/webwork2/courseID/quiz_mode/setID".
- Some LTI authentication mode parameters can now be set in a new tab on the course configuration page. This new tab is available if any of the entries of the @LTIConfigVariables array in /opt/webwork/webwork2/conf/authen_LTI.conf are un-commented.
- There is a new permission "navigation_allowed". This permission can be set on the "Permissions" tab of the course configuration page and is labeled "Allowed to view course home page" there. This permission is intended to be used with LTI authentication when grade passback mode ($LTIGradeMode) is set to "homework". If a user does not have this permission, then the user will not be allowed to view the course home page (the list of homework sets) or the "Grades" page, and links will not be available to access any set other than the one the user signed in to view. Usually this permission would be set to login_proctor in this case. If using this permission, then you will need to ensure that a link is provided to each homework set in your LMS.

### New PG 2.17 Features


- All support for Java and Flash applets has been removed (there is now a warning shown for existing problems).
- Three new graphing tools were added to the GraphTool macro (parserGraphTool.pl): a point tool, a three point quadratic tool, and a four point cubic tool. Furthermore, keyboard controls have been added. This is important for users with mobility impairments, and can be useful for other users having difficulty placing points accurately on the graph.
- The Drag/Drop macro (draggableProof.pl) has been updated, and if problems are written correctly these problems will now work in Gateway quizzes.
- There have been many improvements to Mathquill for both parsing mathematical expressions and units.

### Security/Advanced Features


- The SOAP module is now disabled by default. You will need to set $WeBWorK::SeedCE{soap_authen_key} in /opt/webwork/webwork2/conf/webwork2.apache2.4-config to something secure.
- When hard copies of homework sets are generated, the generated files are no longer placed in a publicly available location on the server. Instead they are generated in the /opt/webwork/webwork2/tmp directory, and served via mod_perl2. Only the user that generates the file will have access to the file over the internet. Furthermore, on successful generation, all files are deleted from the server after the resulting pdf or zip file are served including the served file itself. On failure the files are not deleted so that the user can download them for diagnosis of the failure, but the user will only be able to access those files as long as the page is still open in WeBWorK. See issue #1075 for details on why this change was made.




## WeBWorK 2.16

Source: [https://wiki.openwebwork.org/wiki/Release_notes_for_WeBWorK_2.16](https://wiki.openwebwork.org/wiki/Release_notes_for_WeBWorK_2.16)


### New WeBWorK 2.16 Features


- A new manual problem grader that works for all problems in homework and in gateway quizzes.
- The ability to navigate between students when acting as a student

- A confirmation dialog appears when a student clicks on a timed gateway quiz (but not effective when accessing a quiz from an LMS using LTI)

- Upgrades to the way images are shown to students (resize, zoom, drag)
- Upgraded to MathJax 3 from MathJax 2
- As of 2.15 WeBWorK supports MathQuill for student input.
- ADD_JS_FILE and ADD_CSS_FILE in the PG.pl macro.
- Explanation essays (ask for a regular answer, separately ask for an explanation essay, but the essay part can be globally disabled)
- Rearrange presentation order for homework and quizzes on Homework Sets page (see PR #1282)
- Achievements items need not be single-use, and time based achievements will use the course time-zone setting.
- Major cleanup was done to defaults.config and localOverrides.conf.
- Revised / finer permission settings for the WebworkWebservice (see PR #1163)
- Course level control of support for PG to allow Unicode alternative math symbols etc. (see PR #1174)
- Support for including percentage grades per assignment in CSV output (see PR #1085 and PR #1131 which added a checkbox to include the new data or not). The code depends on the assumption that the total number of points available on an assignment in a constant.
- Passwords are consistently trimmed from leading and trailing white-space, to prevent users from being able to set passwords which could not be used to log in. (see PR #1290)
- Additional improvements and changes can be found on GitHub, and many will appear in the WW 2.16 release planning and testing project board.

### New PG 2.16 Features


- TikZ images in problems.
- Other image support improvements. (see PR #559 and PR #561)
- New macro parserGraphTool.pl for interactive graphing problems. See also GraphTool problem technique.
- "digits" tolType (needs explanation wherever tolerance in general is explained, DigitsTolType problem technique )
- random_coprime and random_pairwise_coprime methods added to PGauxiliaryFunctions.pl (Needs documentation probably in [1].
- PGML can be used in set header files (see PR #1282)
- MathObject2:
- Context classes can have aliases and alternates. (For example variable "X" could be an alias for "x".)
- support for Unicode symbols as alternates to the regular ones.
- see PG PR #518 and webwork2 PR #1174
- Add bypass_equivalence_test switch PR#497
- message_for_blank_answer setting PR#496
- Update answerHints to not produce hints in Preview mode PR#476
- Improvements in efficiency to PGstatisticsmacros.pl.
- Make PG version available to problem code PR#531

### Security/Advanced Features


- Revised "WeBWorK errors" handling options. Option to hide detailed error messages from users but to store them in the error.log file.
- new settings: MIN_HTML_ERRORS JSON_ERROR_LOG
- see PR #1190
- Same-site Cookie support: (see PR #1269, the changed to default to Lax in PR #1307 and the discussion in the older PR #1149.)
- Fix applets in gateway quizzes
- Support for the DBD::MariaDB driver in addition to the DBD::mysql driver. This alternate driver supports both mySQL and MariaDB databases, and is consider to have better UTF-8 support. Using it also seemed to reduce certain types of connection errors.
- As a result, the manner in which the database settings are made in site.conf have also been changed. (See the new version of site.conf.dist.
- See: https://github.com/openwebwork/webwork2/pull/1160, https://github.com/openwebwork/webwork2/issues/1157, https://github.com/openwebwork/webwork2/pull/1150 for more details and background.
- Improvements to LTI integration, and improved debugging
- LMS name and URL in message about needing to access an assignment via the LTI link in the LMS (before the grade passback setting data is available for the user) is now configurable. (see PR #1280 and PR #1285)
- Improved grade passback code, with better debugging features. (see PR #1177)
- The two round process (only update the LMS if the grade changed by at least 0.1 point from 100) is turned on by setting $lti_check_prior = 1; in course.conf (or site wide in conf/authen_LTI.conf).
- A different nonce generation method is used, which may reduce cases of error if a nonce is reused while the LMS still considers it to be recently used.
- However, many of the problems reported as "duplicate nonce" in the forums seems to have been caused by system time being inaccurate on one of the sides.
- Revised WW side nonce handling, and error reporting (see PR #1199)
- Additional security fixes

### Things that were fixed


- Should there be a section like this? For example:

- Fixed bug when Gateway questions were not in sequential order
- Fix bug where, for example, `Formula("-5/(-2 x)")` would display `5/2x` for its text string
- Fix bug with named answer usage. (See Named Answer Rules for the correct way to used named answers so that a problem will work in gateway quizzes. Note that all OPL problems that use named answers are broken for gateway quizzes because they don't do it this way.)
- Fixed bug in MultiAnswer objects with singleResult=>1 which did not properly compute score when setMessage is used. (see PR #524)
- Changes to color support for MathJax 3 controlled equations: PR#1294
