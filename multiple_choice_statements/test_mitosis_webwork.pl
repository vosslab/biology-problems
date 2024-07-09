DOCUMENT();
loadMacros(
  "PGstandard.pl",
  "PGcourse.pl",
  "parserRadioButtons.pl",
);

### BEGIN QUESTION SETUP

#Topic
$topic = "mitosis and meiosis cell division";

# Specify the number of choices to present.
$num_choices = 5;

# Initialize statement arrays.
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

### END QUESTION SETUP

@connecting_words = ('concerning', 'about', 'regarding', 'of', );

# Shuffles an array in place using the Fisher-Yates shuffle algorithm.
sub my_shuffle {
    my @array = @_;
    for (my $i = $#array; $i > 0; $i--) {
        my $j = int random(0, $i, 1.0001);
        next if $i == $j; # Skip unnecessary swaps.
        @array[$i, $j] = @array[$j, $i];
    }
    return @array;
}

# Selects a specified number of unique elements from an array.
sub select_elements {
    my @array = @_;
    my $num_elements = pop @array; # Last element is the number of elements to select.
    my @selected;
    my %seen; # Track indices to ensure uniqueness.

    while (@selected < $num_elements) {
        my $index = int random(0, $#array, 1.0001);
        unless ($seen{$index}++) {
            push(@selected, $array[$index]);
        }
    }
    return @selected;
}

# Selects a specified number of unique elements from an array.
sub select_one_element {
    my @array = @_;
    $element = $array[int random(0, $#array, 1.0001)];
    return $element;
}

# Define a hash with fancy HTML styling for True and False.
%fancy_true_false_map = (
    'True' => '<span style="color: #169179;">TRUE</span>',
    'False' => '<span style="color: #ba372a;">FALSE</span>',
);

# Select one false statement and a set of true statements.
$selected_true_false = select_one_element('True', 'False');
$fancy_true_false = $fancy_true_false_map{$selected_true_false};

$answer_statement = select_one_element(@false_statements);
@selected_true_statements = select_elements(@true_statements, $num_choices - 1);

# Combine and shuffle the choices.
@choices = my_shuffle($answer_statement, @selected_true_statements);

TEXT(beginproblem());

# Setup the radio buttons for the quiz.
$radio = RadioButtons(
    [@choices],
    $answer_statement,
    labels => "ABC",
    randomize => 1,
);

$connecting_word = select_one_element(@connecting_words);

# Display the question.
BEGIN_TEXT
Which one of the following statements is <u><strong>$fancy_true_false</strong></u> $connecting_word $topic?
$BR
\{ $radio->buttons() \}
END_TEXT

# Evaluate the answer.
ANS($radio->cmp());

# Provide the solution.
BEGIN_SOLUTION
The $true_false statement $connecting_word $topic is: [``$answer_statement``].
END_SOLUTION

ENDDOCUMENT();
