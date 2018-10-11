//tip是提示信息，type:'success'是成功信息，'danger'是失败信息,'info'是普通信息

function makeColumnEditable(col) {
    var cont = $(col).html();
    var dd = $('#example').DataTable().row($(col).parents('tr')).data();
    var div = '<div style="display: none;">' + cont + '</div>';  //store the origin value
    var input = '<input class="form-control input-sm"  size="5" value="' + cont + '">';
     $(col).html(div + input);

}

function getRowData()
{
   var $row = $('#newData').parents('tr');
   alert('-------');
   alert($('#newData').val());

}

function ShowMsg(msg) {
    ShowTip(msg, 'info');
}

function ShowSuccess(msg) {
    ShowTip(msg, 'success');
}

function ShowFailure(msg) {
    ShowTip(msg, 'danger');
}

function ShowWarn(msg, $focus, clear) {
    ShowTip(msg, 'warning');
    if ($focus) $focus.focus();
    if (clear) $focus.val('');
    return false;
}