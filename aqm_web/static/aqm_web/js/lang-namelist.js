

PR['registerLangHandler'](
    PR['createSimpleLexer'](
        [
         // A line comment that starts with ;
         [PR['PR_COMMENT'],     /^;[^\r\n]*/, null, ';'],
         // A double quoted, possibly multi-line, string.
         [PR['PR_STRING'],      /^\'(?:[^\'\\]|\\[\s\S])*(?:\'|$)/, null, "'"]
        ],
        [
         [PR['PR_KEYWORD'],     /^(?:&share|&geogrid|&ungrib|&metgrid|&time_control|&domains|&physics|&dynamics|&bdy_control|&namelist_quilt|&chem|&datetime|&io|&interp)\b/, null]
        ]),
    ['namelist']);