$(document).ready(function(){
    
    let favorite = $('#{{item.contentid}}');

    favorite.click(function(){
        var check = $('#{{item.contentid}}').is(':checked');
        let chInt;
        if(check){
            chInt = 1;
        }else{
            chInt = 0;
        }


        $.ajax({
            type : "post",
            url : "/favorite_data",
            data : {
                chInt : chInt,
                contentid : contentid
            },
            success : function(result){
                 print(result);
            },
            error : function(){
                print("오류발생");
            }
        });

    });
         
        



});