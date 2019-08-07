/*global $, SyntaxHighlighter*/

var oTable;


$(document).ready(function () {
	'use strict';

	oTable = $('#entrys_table').dataTable({
        "ajax": '/ajax/get_array',
    }).yadcf([{column_number : 0},
              {column_number : 1, filter_type: "text"},
              {column_number : 2, filter_type: "auto_complete"},
              {column_number : 3, filter_type: "range_number_slider", ignore_char: "-"},
              {column_number : 4}
		], 'tfoot');

	SyntaxHighlighter.all();
});