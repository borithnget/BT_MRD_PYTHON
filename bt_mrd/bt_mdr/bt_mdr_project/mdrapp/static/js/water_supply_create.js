
function visible_control(id_name,is_visible){
    if(is_visible){
        $('#label_'+id_name).show();
        $('#'+id_name).show();
        $('#'+id_name).val(' ');
    }else{
        $('#label_'+id_name).hide();
        $('#'+id_name).hide();
    }
}

