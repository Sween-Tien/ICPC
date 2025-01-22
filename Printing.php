<?php 
    $filename = $argv[1];
    $origname = $argv[2];
    $language = $argv[3];
    $username = $argv[4];
    $teamname = $argv[5];
    $location = $argv[6];
    $lang_remap = array(
        'adb'    => 'ada',
        'bash'   => 'sh',
        'csharp' => 'c',
        'f95'    => 'f90',
        'hs'     => 'haskell',
        'js'     => 'javascript',
        'pas'    => 'pascal',
        'pl'     => 'perl',
        'py'     => 'python',
        'py2'    => 'python',
        'py3'    => 'python',
        'rb'     => 'ruby',
    );
    if (isset($language) && array_key_exists($language, $lang_remap)) {
        $language = $lang_remap[$language];
    }
    $highlight = "";
    if (! empty($language)) {
        $highlight = "-E" . escapeshellarg($language);
    }

    $header = sprintf("Team: %s %s ", $username, $teamname) .
                (!empty($location) ? "[".$location."]":"") .
                " File: $origname||Page $% of $=";
    $tmp = tempnam('/tmp', 'print_'.$username.'_');

    $cmd = "enscript -C " . $highlight
            . " -b " . escapeshellarg($header)
            . " -a 0-10 "
            . " -f Courier11 "
            . " -p $tmp "
            . escapeshellarg($filename) . " 2>&1";
    exec($cmd . " && ps2pdf $tmp $tmp" . ".pdf && rm $tmp && python3 send.py $tmp.pdf", $output, $retval);
    return 0;
?>
