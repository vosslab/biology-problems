DOCUMENT();
loadMacros(
  "PGstandard.pl",
  "PGcourse.pl",
  "parserRadioButtons.pl",
);

### BEGIN QUESTION SETUP FOR INSTRUCTORS

# Define the topic for the question
$topic = "mitosis and meiosis cell division";

# Specify the number of choices to present
$num_choices = 5;

# Initialize statement arrays
@true_statements = (
    "Each daughter cell formed by mitosis has the same kinds of chromosomes as the parent cell",
    "Each daughter cell formed by meiosis has half the number of chromosomes as the parent cell",
    "Mitosis results in two genetically identical daughter cells",
    "Meiosis results in four genetically diverse daughter cells",
    "Mitosis involves one division cycle whereas meiosis involves two division cycles",
);

@false_statements = (
    "Each daughter cell formed by meiosis has the same kinds of chromosomes as the parent cell",
    "Each daughter cell formed by mitosis has half the number of chromosomes as the parent cell",
    "Meiosis results in daughter cells that are genetically identical to the parent cell",
    "Mitosis results in four daughter cells",
    "Meiosis does not contribute to genetic variation in offspring",
);

### END QUESTION SETUP FOR INSTRUCTORS

### BEGIN CODE

# Seed the random number generator for reproducibility
my $seed = time() + $problem_id;
SRAND($seed);

@connecting_words = ('concerning', 'about', 'regarding', 'of');

# Shuffle an array using the Fisher-Yates algorithm
sub my_shuffle {
    my @array = @_;
    for (my $i = $#array; $i > 0; $i--) {
        my $j = int random(0, $i, 1.0001);
        @array[$i, $j] = @array[$j, $i] unless $i == $j; # Perform swap if indices are not the same
    }
    return @array;
}

# Selects a specified number of unique elements from an array
sub select_elements {
    my @array = @_;
    my $num_elements = pop @array;  # Retrieve the number of elements to select
    my @selected;
    my %seen;

    while (@selected < $num_elements) {
        my $index = int(random(0, $#array + 1, 1.001));
        push(@selected, $array[$index]) unless $seen{$index}++;  # Add unique elements
    }
    return @selected;
}

# Select one element from an array
sub select_one_element {
    my @array = @_;
    return $array[int(random(0, $#array + 1, 1.001))];
}

# HTML styling for True and False responses
%fancy_true_false_map = (
    'True' => '<span style="color: #169179;">TRUE</span>',
    'False' => '<span style="color: #ba372a;">FALSE</span>',
);

# Process selections for the quiz
$selected_true_false = select_one_element('True', 'False');
$fancy_true_false = $fancy_true_false_map{$selected_true_false};

if ($selected_true_false eq 'False') {
    $answer_statement = select_one_element(@false_statements);
    @selected_statements = select_elements(@true_statements, $num_choices - 1);
} elsif ($selected_true_false eq 'True') {  # Use `elsif` instead of `else if`
    $answer_statement = select_one_element(@true_statements);
    @selected_statements = select_elements(@false_statements, $num_choices - 1);
}

# Shuffle the final choices for display
@choices = my_shuffle($answer_statement, @selected_statements);

TEXT(beginproblem());

# Setup radio buttons for response
$radio = RadioButtons(
    [@choices],
    $answer_statement,
    labels => "ABC", # Label the choices with letters
    displayLabels => 1, # Display labels next to the radio buttons
    labelFormat => '${BBOLD}%s.${EBOLD} ', # Customize label format
    separator => '<div style="margin-bottom: 0.7em;"></div>', # Custom spacing using a div with margin
    uncheckable => 1, # Allow unchecking by re-clicking
    randomize => 1,
);

$connecting_word = select_one_element(@connecting_words);

# Display the question
BEGIN_TEXT
<p>Which one of the following statements is <u>${BBOLD}$fancy_true_false${EBOLD}</u> $connecting_word $topic?</p>
\{ $radio->buttons() \}
END_TEXT

# Evaluate the answer
ANS($radio->cmp());

# Solution feedback
BEGIN_SOLUTION
The $fancy_true_false statement $connecting_word $topic is: "<i>$answer_statement</i>".
END_SOLUTION

### END CODE

ENDDOCUMENT();
