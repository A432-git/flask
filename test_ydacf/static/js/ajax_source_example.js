/*global $, SyntaxHighlighter*/

var oTable;


$(document).ready(function () {
	'use strict';

	oTable = $('#entrys_table').dataTable({
        "ajax": '/ajax/get_dm_array',
    }).yadcf([
	    {column_number : 0, filter_type: "multi_select", select_type: 'select2'},
	    {column_number : 1,select_type: 'select2'},
	    {column_number : 2, select_type: "multi_select", select_type: 'select2'},
	    {column_number : 3, filter_type: "range_number_slider"},
//	    {column_number : 4, filter_type: "text", text_data_delimiter: ",", exclude: true},

	    ]);

	SyntaxHighlighter.all();
});