$( document ).ready(function() {
    //show on hpopover over
    $(function () {
        $('[data-toggle="popover"]').popover()
      });

    $('#image').click(function(){
        $('#myfile').click()
    });
    //call delete function when press this button
    $('.delete_btn').click(function(){
        //Display message to user if press delete button
        //with an OK and a Cancel button
        var type_name = $(this).val();
        var confirm_msg = confirm("Are you sure to delete this item?");
        if(confirm_msg){   
             $.ajax({
                 url: "delete",
                 method:"GET",
                 data:{
                    type_name
                 },
                 
                 success: function(){
                    console.log(type_name);
                    //find class type whose data-value equal to value of pressed button
                    var $div = $(".types").filter(function() {
                        return $(this).data("value") == type_name; // where value == type_name to find
                    });
                    $div.fadeOut(1000);  
                    //Reload page 
                    window.location.reload();        
                   
              }});
        }
    });
    //call addzakah function when press this button
    $('.add_btn').click(function(){
        let modal_body = document.getElementById('modalbody');
        //Display message to user if press delete button
        //with an OK and a Cancel button
             $.ajax({
                 url: "add", 
                 success: function(response){
                    console.log(response);   
                    const obj = response.choose_types;
                    // console.log(obj); 
                    console.log('add');
                    if (obj.length === 0) {
                        if (modal_body.innerHTML.trim() == "") {
                            modal_body.innerHTML +=
                            "<div class='col-md-10 d-flex justify-content-center'>"+
                            "<h6 class='text-center arabic-text'>تم إضافة كل أنواع الصدقة  </h6>"+
                            "</div>";
                        }
          
                      }else{
                        if (modal_body.innerHTML.trim() == "") {
                            //do something
                        obj.forEach(el => {
                            console.log(el.name_en);
                            
                            modal_body.innerHTML+=
                           
                            " <div class='col-md-4'>"+
                                "<section class='app text-center'>"+
                                    "<article class='feature1' id='myDiv'>"+
                                    "<input type='checkbox' id='feature1' name='zakah'"+ "value='"+el.name_en+":"+el.name_ar+":"+el.type_id+"'/>"+
                                    "<div>"+
                                        "<span>"+
                                       "<p class='english-text' style='margin-bottom: 0;'>"+el.name_en+"</p>"+
                                        "<p class='arabic-text' style='margin-bottom: 0;'>"+el.name_ar+"</p>"+
                                        "</span>"+
                                    "</div>"+
                                    "</article>"+
                                "</section>"+
                                "</div>"
                            
                        });
                   //if
                        }

                      }
                      
                   
        //Sucess    
             }

           //ajax 
            });
               //save checkedbox value in array
               $('.add').on('click', function() {

                var myCheckboxes = new Array();
                
                $('[name="zakah"]').each(function(i,e) {
                    if ($(e).is(':checked')) {
                        myCheckboxes.push($(this).val());
                    }
                });
                
                console.log(myCheckboxes);
                const myJSON = JSON.stringify(myCheckboxes);
                console.log(myJSON);
                $.ajax({
                    type: "GET",
                    url: "add",
                    data: {
                      'myCheckboxes': myJSON
                    },
                    success: function(){
                    $("#close-btn").click();
                    window.location.reload(); 
                }});
                
             });
         
    });
  
     //getData and send it to add_Charity function in view 
     $('.AddChar').on('click', function() {  
         var CharData = [];
         var CharUser = $.trim($('#user_char').val());
         if(CharUser.length === 0){
            $('#alert-char-add-user').css("display","block");
            console.log('emptyuser');
         }
         var CharPass= $.trim($('#char_pass').val());
         if(CharPass.length === 0){
            $('#alert-char-add-pass').css("display","block");
            console.log('emptypassword');
         }
         console.log('getData',CharUser,CharPass);
         console.log('getData');
         if (CharUser.length > 0 && CharPass.length >0 ) {
         CharData.push(CharUser,CharPass);
         console.log(CharData);
         var myJSONData = JSON.stringify(CharData);
         console.log(myJSONData);
         $.ajax({
            type: "GET",
            url: "admindashboard/addchar",
            data: {
              'myJSONData': myJSONData
            },
            success: function(){
                console.log('sendCharData');
                //call close button to close model 
                $("#closeChar").click();
                $('#user_char').val('');
                $('#char_pass').val('');
                window.location.reload();        
          }});
         
         }
     });
//clear input and hide alert message when click close button in model
     $('.close-fromchar').on('click', function(){  
        $('#user_char').val('');
        $('#char_pass').val('');
        $('#alert-char-add-user').css("display","none");
        $('#alert-char-add-pass').css("display","none");
      });

    //call Edit_charity function when press this button
    $('.edit_char').on('click', function() {   
        var charuser_pass = $(this).val().split(",");
        var charu = charuser_pass[0];
        var charp= charuser_pass[1];
        var charname_en= charuser_pass[2];
        var charname_ar= charuser_pass[3];
        var CharData = [];
        console.log('charuser_pass:',charuser_pass,typeof(charuser_pass));
        console.log('charuser_pass:',charu,charp)
        $('#username_char').val(charu);
        $('#passchar').val(charp);
        $('#name_ar4char').val(charname_ar);
        $('#name_en4char').val(charname_en);
        $('#editmychar').click(function (e) {
            if (e.target) {
               var username_char = $('#username_char').val();
               var passchar = $('#passchar').val();
               var arnamechar = $('#name_ar4char').val();
               var ennamechar = $('#name_en4char').val();
               if(arnamechar.length === 0){
                $('#alert-char-ar-n').css("display","block");
                console.log('emptychar_ar_name');
             }
             if(ennamechar.length === 0){
                $('#alert-char-en-n').css("display","block");
                console.log('emptychar_ar_name');
             }
             if (ennamechar.length > 0 && arnamechar.length >0) {
               CharData.push(username_char,passchar,charu,ennamechar,arnamechar);
               console.log(CharData);
               var myJSONData = JSON.stringify(CharData);
               console.log(myJSONData);
               $.ajax({
                type: "GET",
                url: "admindashboard/editchar",
                data: {
                  'myJSONData': myJSONData
                },
                success: function(){
                    console.log('sendCharData');
                    $("#close-fromEditchar").click();
                    window.location.reload();  
              }});
            }
            }
        });
    });
    //clear input and hide alert message when click close button in model
    $('#closechar4edit').on('click', function(){  
        $('#alert-char-ar-n').css("display","none");
        $('#alert-char-en-n').css("display","none");
      });
    //call delete charity function when press this button
    $('.delete_char').click(function(){
        //Display message to user if press delete button
        //with an OK and a Cancel button
        var char_username = $(this).val();
        var confirm_msg = confirm("Are you sure to delete this item?");
        if(confirm_msg){   
             $.ajax({
                 url: "admindashboard/deletechar",
                 method:"GET",
                 data:{
                    char_username
                 },
                 
                 success: function(){
                    console.log(char_username);
                    //find class type whose data-value equal to value of pressed button
                    var $div = $(".types").filter(function() {
                        return $(this).data("value") == char_username; // where value == type_name to find
                    });
                    $div.fadeOut(1000);  
                    //Reload page 
                    window.location.reload();        
                   
              }});
        }
    });

    //getData and send it to add_Dev function in view 
    $('.AddDev').on('click',function() {  
        var DevData = [];
        var DevUser = $('#devName').val();
        var DevPass=  $('#devPass').val();
        var DevMac=   $('#devMac').val();
        if(DevUser.length === 0){
            $('#alert-dev-name').css("display","block");
            console.log('emptyDevUser');
         }
         if(DevPass.length === 0){
            $('#alert-dev-pass').css("display","block");
            console.log('emptyDevPass');
         }
        console.log('getDevData',DevUser,DevPass,DevMac);
        if (DevUser.length > 0 && DevPass.length >0) {
        DevData.push(DevUser,DevPass,DevMac);
        console.log(DevData);
        var myJSONData = JSON.stringify(DevData);
        console.log(myJSONData);
        $.ajax({
           type: "GET",
           url: "admindashboard/addDevice",
           data: {
             'myJSONData': myJSONData
           },
           success: function(){    
            console.log('sendDevData');
            $("#closeDev").click();
             window.location.reload();  
         }});
        } 
    });
//clear input and hide alert message when click close button in model
$('#close4adddev').on('click', function(){  
        $('#devName').val('');
        $('#devPass').val('');
        $('#alert-dev-name').css("display","none");
        $('#alert-dev-pass').css("display","none");
});

//call delete device function when press this button
    $('.delete_dev').click(function(){
        //Display message to user if press delete button
        //with an OK and a Cancel button
        var dev_name = $(this).val();
        var confirm_msg = confirm("Are you sure to delete this item?");
        if(confirm_msg){   
             $.ajax({
                 url: "admindashboard/deletedev",
                 method:"GET",
                 data:{
                    dev_name
                 },                
                 success: function(){
                    console.log(dev_name);
                    //find class type whose data-value equal to value of pressed button
                    var $div = $(".types").filter(function() {
                    return $(this).data("value") == dev_name; // where value == type_name to find
                    });
                    $div.fadeOut(1000);  
                    //Reload page 
                    window.location.reload();                        
              }});
        }
    });  
   

//call assign device function 
$('.assign_dev').click(function(){ 
    var device_name = $(this).val().split(",");
    var devu = device_name[0];
    var devp= device_name[1];
    var devstatus= device_name[2];
    var charity_name = device_name[3]
    var start_date = device_name[4]
    var maintain_date = device_name[5]
    console.log('device_name',device_name,'devstatus',devstatus,charity_name,start_date)
    $('#devnamefromedit').val(devu);
    $('#devpassfromedit').val(devstatus);
    if (devstatus == 1){
        $("#devstatus option:first").html("يعمل");
        $("#devstatus option:first").val(1);
        $("#devstatus option:last").html("لا يعمل");
        $("#devstatus option:last").val(0);
    }else{
        $("#devstatus option:first").html("لا يعمل");
        $("#devstatus option:first").val(0);
        $("#devstatus option:last").html("يعمل");
        $("#devstatus option:last").val(1);
    }
    $("#getchaN option:first").html(charity_name);
    $("#getchaN option:first").val(charity_name);
    getchaN
    var DevData = [];
    var device_EditmainDate = $('#devEditmdate').val(maintain_date);
    // var charN = $('#getchaN option:selected').val();
    var charN = $('#getchaN').val();
    console.log(charN);
    var devsatus = $('#devstatus').val();
    // console.log(devsatus);
    var devStartDate = $('#devstartdate').val(start_date);
    console.log(devStartDate);
    var NewdevStartDate = start_date;
    $("#devstartdate").on("change", function() {
        // Get the new date value
        NewdevStartDate = $(this).val();
    });
   
    var startNewMainDate = new Date(maintain_date);
    var endNewMainDate   = new Date(startNewMainDate.setFullYear(startNewMainDate.getFullYear() + 1));
    var Newdevice_EditmainDate = endNewMainDate.toISOString().slice(0, 10);
    $('#NextMaintanance').val(Newdevice_EditmainDate)

    $("#devEditmdate").on("change", function() {
        Newdevice_EditmainDate = $(this).val();
        var startDate = new Date(Newdevice_EditmainDate);
        // Calculate date after one year
        var endDate = new Date(startDate.setFullYear(startDate.getFullYear() + 1));
        // Format the date to yyyy-mm-dd
        var formattedEndDate = endDate.toISOString().slice(0, 10);
        $('#NextMaintanance').val(formattedEndDate)
        console.log(formattedEndDate); // Output the calculated date
    });
    console.log(' $("#devEditmdate").val()',$("#devEditmdate").val())
    $('#assignDev').click(function (e) {
        if (e.target) 
    {
        console.log('charN',$('#getchaN').val());
        console.log('devstatus',$('#devstatus').val());

       if($('#devnamefromedit').val().length === 0){
          $('#alert-devEdit-name').css("display","block");
          console.log('emptyalert-devEdit-name');
      }
      if($('#getchaN option:selected').val() === ''){
          $('#alert-devEdit-char').css("display","block");
       console.log('emptyalert-devEdit-char');
       }
        if( $('#devstatus option:selected').val() === ''){
             $('#alert-devEdit-status').css("display","block");
             console.log('emptyalert-devEdit-status');
        }
        if( $('#devstartdate').val() === ''){
           $('#alert-devEdit-sdate').css("display","block");
          console.log('emptyalert-devEdit-startdate');
      }
      if( $('#devEditmdate').val() === ''){
          $('#alert-devEdit-mdate').css("display","block");
          console.log('emptyalert-devEdit-maintainancedate');
     }
     console.log('NewdevStartDate',NewdevStartDate)
   if ($('#getchaN option:selected').val().length > 0 && $('#devstatus').val().length > 0 && $('#devstartdate').val().length > 0 && $('#devEditmdate').val().length > 0 && $('#devnamefromedit').val().length > 0)  {   
        
        DevData.push($('#getchaN').val(),$('#devstatus').val(),NewdevStartDate,$('#devnamefromedit').val(),Newdevice_EditmainDate, $('#NextMaintanance').val(),devu);
        console.log(DevData);
        console.log('device_name:',device_name);
      var myJSONData = JSON.stringify(DevData);
     $.ajax({
           type: "GET",
            url: "admindashboard/assigndev",
            data: {
            'myJSONData': myJSONData
            },
            success: function(){
            $("#closeeditedev").click();
            window.location.reload(); 
            console.log('sendDevDataforupdate');
            
        }});
    }
}
 });
});
$('#closeassidnudev').on('click', function(){  
    // $('#devEditmdate').val('');
    // $('#devstartdate').val('');
    $('#getchaN').val( $('#getchaN').find("option[selected]").val());
    $('#devstatus').val( $('#devstatus').find("option[selected]").val());
    $('#alert-devEdit-name').css("display","none");
    $('#alert-devEdit-char').css("display","none");
    $('#alert-devEdit-status').css("display","none");
    $('#alert-devEdit-sdate').css("display","none");
    $('#alert-devEdit-mdate').css("display","none");
});





//call between2Dates_Statistics function 
$('#search-date').click(function(){ 
    var today = new Date().toISOString().split('T')[0];
    var between2Dates = [];
    var Get_date_1 = $('#filterDateone').val();
    var Get_date_2 = $('#filterDatetwo').val();
    if(Get_date_1.length === 0){
        $('#alert-dateone').css("display","block");
        console.log('emptydate1');
     }
    if(Get_date_2.length === 0){
        $('#alert-datetwo').css("display","block");
        console.log('emptydate2');
     }
      between2Dates.push($('#filterDateone').val(),$('#filterDatetwo').val());
      console.log(between2Dates);
      var myJSONData = JSON.stringify(between2Dates);
     $.ajax({
           type: "GET",
            url: "senddate",
            data: {
            'myJSONData': myJSONData
            },
            success: function(response){
            //  $("#close-datebtn").click();
            console.log('myJSONData',myJSONData);
            console.log('senddates');
            console.log(response);
            console.log('response.filter_sum',response.filter_sum)
            $('.between2Dates_num').html(response.filter_num);
            $('.between2Dates_numSum').html(response.filter_sum);
            $('#response').css("display","block");    
        }});
        $('#close-datebtn').click(function (e) {
            if (e.target) 
        {
            $('#filterDateone').val(today);
            $('#filterDatetwo').val(today);
            $('#between2Dates_num').html();
            $('#between2Dates_numSum').html();
            $('#response').css("display","none"); 
        }
    });

});
//search by month 
$('#search-month').click(function() {
    if ($('#gMonth option:selected').val().length > 0){
        var month = $('#gMonth').val();
        console.log("month",month);
    }
    if ($('#yearSelect option:selected').val().length > 0){
        var year = $('#yearSelect').val();
        console.log("year",year);
    }
    $.ajax({
        type: "GET",
         url: "sendmonth",
         data: {
         'month': month,
         'year':year
         },
         success: function(response){
         console.log('sendmonthYear');
         console.log(response);
         console.log('response.filter_sum',response.filter_sum)
        $('#betweenmonth_year').html(response.filter_num);
        $('#between_monthYear_numSum').html(response.filter_sum);
        $('#response-monthYear').css("display","block"); 
        
         
     }});
     $('#close-monthYearbtn').click(function (e) {
        if (e.target) 
    {
        $('#gMonth').val('');
        $('#yearSelect').val('');
        $('#betweenmonth_year').html();
        $('#between_monthYear_numSum').html();
        $('#response-monthYear').css("display","none"); 
    }
});
});
//Add Zaakah from charity side
$("#Addotherzakah").click(function(){
    if ($('#otherzakah_en').val().length == 0 ){$('#otheralert-zakah_en').css("display","block")}
    if ($('#otherzakah_ar').val().length == 0 ){$('#otheralert-zakah_ar').css("display","block")}
    if ($('#otherzakah_ar').val().length > 0 && $('#otherzakah_en').val().length > 0 ){    
        zakah_en = $('#otherzakah_en').val();
        zakah_ar = $('#otherzakah_ar').val();
        console.log('zakah_en&zakah_ar',zakah_en,zakah_ar)
        $.ajax({
            url: "addzakahch",
            data: {
            'zakah_en': zakah_en,
            'zakah_ar':zakah_ar
            },
            success: function(response){
                if (response == 1){
                    $('#otheralert-type').css("display","block")
                    console.log(response);    
                }
                if(response == 0){
                    $('#otherzakah_en').val('');
                    $('#otherzakah_ar').val('');
                    $('#otheralert-zakah_en').css("display","none")
                    $('#otheralert-zakah_ar').css("display","none")
                    $('#closeotherzakah').click();
                    window.location.reload();    
                }   
         }}); 
    }
}); 

// Add zakah type from admin
    //call addzakah function when press this button
    $('#zakah-tab').click(function(){
        var arrzakahsubtype=[]
        //Display message to user if press delete button
        //with an OK and a Cancel button
        let row = document.getElementById('zak'); 
        $.ajax({
            url: "admindashboard/displayzakah", 
            success: function(response){
               console.log(response);   
               const obj = response.all_types;
               // console.log(obj); 
               console.log('displayzakah');
               if (row.innerHTML.trim() == "") {
                   //do something
               obj.forEach(el => {
                   console.log(el.name_en);   
                   row.innerHTML+=
                   "<div class='col-md-4'>"+
                   "<div class='types' data-value='"+el.name_en+"'" +"style='padding-left:10px;padding-right: 10px;margin-bottom: 20px;'>"+
                    "<span class='d-inline-block' data-toggle='popover' data-trigger='hover' data-placement='top' data-content='احذف زكاة' data-trigger='hover'>"+
                      "<button class='delete_zakah' value='"+el.name_en+"'"+">"+"<i class='fas fa-trash'></i></button>"+
                    "</span>"+
                    "<span class='d-inline-block' data-toggle='popover' data-trigger='hover' data-placement='top' data-content='تحديث زكاة' data-trigger='hover'>"+
                    "<button class='edit_zakah' data-toggle='modal' data-target='#Editzakah' value='"+el.id+","+el.name_en  +","+ el.name_ar +"'"+" style='border: none;background: none;'>"+
                   "<i class='far fa-edit'></i>"+
                    "</button>"+
                  "</span>"+
                  "<p class='text-center english-text' style='margin-bottom: 0;'>"+el.name_en+"</p>"+
                  "<p class='text-center arabic-text'  style='margin-bottom: 0;'>"+el.name_ar+"</p>"+
                  "<div>"+
                  " <span class='d-inline-block' data-toggle='popover' data-trigger='hover' data-placement='top' data-content='اضف صدقة فرعية' data-trigger='hover'>"+
                           "<button data-toggle='modal' data-target='#addSubmodalzakah' class='addSub_zakah' id='subzakahadd' value='"+el.id+"'"+">"+"<i class='fas fa-plus'></i></button>"+
                    "</span>"+
                    " <span class='d-inline-block' data-toggle='popover' data-trigger='hover' data-placement='top' data-content='استعرض صدقة فرعية' data-trigger='hover'>"+
                    "<button type='submit' class='ViewSub_zaka4admin' value='"+el.id+"'"+">"+
                    "<i class='fas fa-eye' style='color: #fff;'></i>"+
                  "</button>"+
                  "</span>"
                    "</div>"
                   "</div>"+
                  "</div>" 
               });
          //if
        }
    //Sucess    
        }
      //ajax 
       });
        
        $('#Addzakah').click(function (e) { 
        if (e.target) {
        if ($('#zakah_en').val().length == 0 ){$('#alert-zakah_en').css("display","block")}
        if ($('#zakah_ar').val().length == 0 ){$('#alert-zakah_ar').css("display","block")}
        
        if ($('#zakah_en').val().length > 0 && $('#zakah_ar').val().length > 0 ){    
            zakah_en = $('#zakah_en').val();
            zakah_ar = $('#zakah_ar').val();
         
        $.ajax({
            type: "GET",
                url: "admindashboard/displayzakah",
                data: {
                'zakah_en': zakah_en,
                'zakah_ar':zakah_ar,
                
                },
                success: function(response){
               console.log(response);   
               const obj = response.all_types;
                $("#closezakah").click();
                row.innerHTML="";
                if (row.innerHTML.trim() == "") {
                    //do something
                obj.forEach(el => {
                    console.log(el.name_en);   
                    row.innerHTML+=
                    "<div class='col-md-4'>"+
                    "<div class='types' data-value='"+el.name_en+"'" +"style='padding-left:10px;padding-right: 10px;margin-bottom: 20px;'>"+
                     "<span class='d-inline-block' data-toggle='popover' data-trigger='hover' data-placement='top' data-content='احذف زكاة' data-trigger='hover'>"+
                       "<button class='delete_zakah' value='"+el.name_en+"'"+">"+"<i class='fas fa-trash'></i></button>"+
                     "</span>"+
                     "<span class='d-inline-block' data-toggle='popover' data-trigger='hover' data-placement='top' data-content='تحديث زكاة' data-trigger='hover'>"+
                     "<button class='edit_zakah' data-toggle='modal' data-target='#Editzakah' value='"+el.id+","+el.name_en  +","+ el.name_ar +"'"+" style='border: none;background: none;'>"+
                    "<i class='far fa-edit'></i>"+
                     "</button>"+
                   "</span>"+
                   "<p class='text-center english-text' style='margin-bottom: 0;'>"+el.name_en+"</p>"+
                   "<p class='text-center arabic-text'  style='margin-bottom: 0;'>"+el.name_ar+"</p>"+
                   "<div>"+
                   " <span class='d-inline-block' data-toggle='popover' data-trigger='hover' data-placement='bottom' data-content='اضف صدقة فرعية' data-trigger='hover'>"+
                   "<button data-toggle='modal' data-target='#addSubmodalzakah' id='subzakahadd' class='addSub_zakah' value='"+el.id+"'"+">"+"<i class='fas fa-plus'></i></button>"+
                   "</span>"+
                    "</div>"+
                    "</div>"+
                   "</div>" 
                });
           //if
         }
                $('#zakah_en').val('');
                $('#zakah_ar').val('');
                $('#alert-zakah_en').css("display","none")
                $('#alert-zakah_ar').css("display","none")
                console.log("zakah_en",zakah_ar)
                $("#zakah-tab").click(); 

        }});  
     
    } //if input text not empty
    
        }});//end Addzakah function
        $('#close-zakah').click(function (e) {
            if (e.target) 
        {
            $('#zakah_en').val('');
            $('#zakah_ar').val('');
            $('#alert-zakah_en').css("display","none")
            $('#alert-zakah_ar').css("display","none")
            $("#zakah-tab").click(); 

        }
    });
            
    }); //end #zakah-tab function
             
  //Add Subzakah
  $(document).on('click', '#subzakahadd', function(){
        var zakahid = $(this).val();
        console.log('subzakahadd ',subzakahadd)
        console.log('zakahid ',zakahid)
        $('#Addsubzakah').click(function (e) {
            if (e.target) {
            console.log('Addsubzakah')
            if ($('#zakah_subar').val().length == 0 ){$('#alert-zakah_subar').css("display","block")}
            if ($('#zakah_suben').val().length == 0 ){$('#alert-zakah_suben').css("display","block")}

            if ($('#zakah_subar').val().length > 0 && $('#zakah_suben').val().length > 0 ){    
                zakah_suben = $('#zakah_suben').val();
                zakah_subar = $('#zakah_subar').val();
                console.log(zakah_suben,zakah_subar)
             
            $.ajax({
                type: "GET",
                    url: "admindashboard/addSubZakah",
                    data: {
                    'zakah_suben': zakah_suben,
                    'zakah_subar':zakah_subar,
                    'zakahid':zakahid
                    
                    },success: function(response){
                        if (response=="add"){
                            $('#zakah_suben').val('');
                            $('#zakah_subar').val('');
                            $('#alert-zakah_subar').css("display","none")
                            $('#alert-zakah_suben').css("display","none")
                            $('#alert-zakasubexit').css("display","none")
                            $("#closesubzakah").click()
                            $("#zakah-tab").click(); 
                            console.log('ressponse',response)
                        }
                        if (response=="exit"){
                            $('#alert-zakah_subar').css("display","none")
                            $('#alert-zakah_suben').css("display","none")
                            $('#alert-zakahsubexit').css("display","block")
                            console.log('ressponse',response)
                        
                        }
            }});   
         
        } 
           
        }
        $('#close-subtypezakah').click(function (e) {
            if (e.target) 
        {
            $('#zakah_suben').val('');
            $('#zakah_subar').val('');
            $('#alert-zakah_subar').css("display","none")
            $('#alert-zakah_suben').css("display","none")
            $("#zakah-tab").click(); 

        }
    });
    });
        
  
  })


//Delete zakah type 
$(document).on('click', '.delete_zakah', function(){
    console.log("delete_zakah clicked");
    var zakah_name_en = $(this).val();
    var confirm_msg = confirm("Are you sure to delete this item?");
    if(confirm_msg){   
         $.ajax({
             url: "admindashboard/deleteZakah",
             method:"GET",
             data:{
                zakah_name_en
             },                
             success: function(){
                console.log(zakah_name_en);
                //find class type whose data-value equal to value of pressed button
                var $div = $(".types").filter(function() {
                return $(this).data("value") == zakah_name_en; // where value == type_name to find
                });
                $div.fadeOut(1000);  
                //Reload page 
                $("#zakah-tab").click();                     
          }});
    }
});  

 


//Edit zakah type 
$(document).on('click', '.edit_zakah', function(){
    let row = document.getElementById('zak');
    console.log("Edit zakah clicked");
    var Eidit_Zakah_name = $(this).val().split(",");
    var Z_id = Eidit_Zakah_name[0];
    var Zname_en = Eidit_Zakah_name[1];
    var Zname_ar= Eidit_Zakah_name[2];
    data =[]
    console.log('Edit_Zakah_name',Eidit_Zakah_name)
    $('#Eidtzakah_en').val(Zname_en);
    $('#Eiditzakah_ar').val(Zname_ar);
    $('#EidtZakah_type').click(function (e) {
        if (e.target) 
    {
        if($('#Eiditzakah_ar').val()==''){$('#alert-Edit_zakah_ar').css("display","block")};
        if($('#Eidtzakah_en').val()==''){$('alert-Eidit_zakah_en').css("display","block")};
        if($('#Eiditzakah_ar').val().length>0 && $('#Eidtzakah_en').val().length>0){
            data.push(Z_id,$('#Eidtzakah_en').val(),$('#Eiditzakah_ar').val());
            console.log("Edit zakah data",data);
            var myJSONData = JSON.stringify(data);
            $.ajax({
                type: "GET",
                    url: "admindashboard/editZakah",
                    data: {
                    'myJSONData': myJSONData
                    },
                    success: function(response){
                    //  $("#close-datebtn").click();
                    console.log('myJSONData',myJSONData);
                    console.log('Edit zakah type');
                    console.log('All type response',response);
                    const obj = response.Edit_all_types;
                    $("#CloseZakah_type").click();
                    row.innerHTML="";
                    if (row.innerHTML.trim() == "") {
                        obj.forEach(el => {
                            console.log(el.name_en);   
                            row.innerHTML+=
                            "<div class='col-md-4'>"+
                            "<div class='types' data-value='"+el.name_en+"'" +"style='padding-left:10px;padding-right: 10px;margin-bottom: 20px;'>"+
                             "<span class='d-inline-block' data-toggle='popover' data-trigger='hover' data-placement='top' data-content='احذف زكاة' data-trigger='hover'>"+
                               "<button class='delete_zakah' value='"+el.name_en+"'"+">"+"<i class='fas fa-trash'></i></button>"+
                             "</span>"+
                             "<span class='d-inline-block' data-toggle='popover' data-trigger='hover' data-placement='top' data-content='تحديث زكاة' data-trigger='hover'>"+
                             "<button class='edit_zakah' data-toggle='modal' data-target='#Editzakah'  value='"+el.id+","+el.name_en  +","+ el.name_ar +"'"+" style='border: none;background: none;'>"+
                            "<i class='far fa-edit'></i>"+
                             "</button>"+
                           "</span>"+
                           "<p class='text-center english-text' style='margin-bottom: 0;'>"+el.name_en+"</p>"+
                           "<p class='text-center arabic-text'  style='margin-bottom: 0;'>"+el.name_ar+"</p>"+
                            "</div>"+
                           "</div>" 
                        });
                    }
                
                       
                }});
        }//if input value not empty
    }//If button click
});// button click
});

$('#device-tab').click(function(){ 
    let rowfromjquery = document.getElementById('rowfromjquery'); 
    console.log('clicked');
    $(document).on('click', '#edit_devN', function(e){
     if (e.target){
        var device_details = $(this).val().split(",");
        var devid = device_details[0];
        var devname= device_details[2];
        var devcity= device_details[3];
        var devaddress= device_details[4];
        $('#Edit_DveN4char').val(devname);
        $('#Edit_Dvea4char').val(devaddress);
        $("#citySelect").val(devcity).change();
        console.log('device_details',device_details);
        console.log('clicked from edit_devN');
   
    $(document).on('click', '#Edit_dev_N', function(e){
    if (e.target) {
        console.log('clicked from Edit_dev_N');
        if( $('#Edit_DveN4char').val() == ''){$('#alert-DevN').css("display","block");}
        if( $('#citySelect').val() == ''){$('#alert-OmanCity').css("display","block");}
        if( $('#Edit_DveN4char').val().length > 0 && $('#citySelect').val().length >0 ){
           
        $.ajax({
        type: "GET",
        url: "dispalyDev4char",
        data: {
       'devid':devid,
       'NewdevName': $('#Edit_DveN4char').val(),
       'city':$('#citySelect option:selected').val(),
       'address':$('#Edit_Dvea4char').val(),
        },
       //if success
       success: function(response){
        console.log('response',response);
        const obj = response.all_dev_4Char;
        rowfromjquery.innerHTML="";
        if (rowfromjquery.innerHTML.trim() == "") {
            obj.forEach(el => {
                if (el.check_name == 1){
                    
                    $("#devX").click();

                }
                // else{ 
                //     $('#dispalymsg').css("display","none")
                //     $("#devX").click();
                // }
            rowfromjquery.innerHTML+=
            "<div class='col-md-4'>"+
            "<div class='types' style='background-color: #009146;color: #fff;'>"+
            "<span class='d-inline-block' data-toggle='popover' data-trigger='hover' data-placement='top' data-content='تحديث بيانات الجهاز' data-trigger='hover'>"+
            "<button id='edit_devN' class='btn' data-toggle='modal' data-target='#EditDevice4CharModal'"+ "value='"+el.devId+","+el.charity_id+","+el.name+","+el.city+","+el.address+"'>"+
            "<i class='far fa-edit'  style='color: #fff;'></i>"+
            "</button>"+
            "</span>"+
            "<p class='text-right arabic-text'  style='margin-bottom: 0;'>"+
            "<span>"+ el.name+"</span>"+"<span class='arabic-text' style='margin-left: 20px;margin-right: 20px;'>اسم الجهاز</span>"+
            "</p>"+
            "<p class='text-right arabic-text' style='margin-bottom: 0;'>"+
            "<span class='arabic-text' style='margin-left: 20px;margin-right: 20px;'>الولاية</span><span>"+ el.city+"</span>"+
            "</p>"+
            "<p class='text-right arabic-text' style='margin-bottom: 0;'>"+
            "<span class='arabic-text' style='margin-left: 20px;margin-right: 20px;' dir='rtl'>العنوان</span><span dir='rtl'>"+ el.address+"</span>"+
            "</p>"+
            "<p class='text-right arabic-text'  style='margin-bottom: 0;'>"+
            "<span>"+ el.start_date+"</span>"+"<span class='arabic-text' style='margin-left: 20px;margin-right: 20px;'>تاريخ البدء  </span>"+
            "</p>"+
            "<p class='text-right arabic-text'  style='margin-bottom: 0;'>"+
            "<span>"+ el.last_maintenance+"</span>"+"<span class='arabic-text' style='margin-left: 20px;margin-right: 20px;'>تاريخ الصيانة  </span>"+
            "</p>"+
            "<p class='text-right arabic-text'  style='margin-bottom: 0;'>"+
            "<span>"+ el.num_of_trans+"</span>"+"<span class='arabic-text' style='margin-left: 20px;margin-right: 20px;'>عدد التبرعات</span>"+
            "</p>"+
            "<p class='text-right arabic-text'  style='margin-bottom: 0;'>"+
            "<span>"+ el.sum+"</span>"+"<span class='arabic-text' style='margin-left: 20px;margin-right: 20px;'>مجموع التبرعات</span>"+
            "</p>"+
            "</div>"+"</div>"
            });
        }

}});//Ajax
}
}
});//Button
//check if close button pressed 
$('#XcloseDevN_4Char').click(function(e){ 
    if (e.target) {
        $('#dispalymsg').css("display","none");
        $('#alert-DevN').css("display","none");
        $('#alert-OmanCity').css("display","none");

    }

});
}
});  
    $.ajax({
        type: "GET",
            url: "dispalyDev4char",
            success: function(response){
            console.log('response',response);
            const obj = response.all_dev_4Char;
            rowfromjquery.innerHTML="";
            if (rowfromjquery.innerHTML.trim() == "") {
                obj.forEach(el => {
                rowfromjquery.innerHTML+=
                "<div class='col-md-4'>"+
                "<div class='types' style='background-color: #009146;color: #fff;'>"+
                "<span class='d-inline-block' data-toggle='popover' data-trigger='hover' data-placement='top' data-content='تحديث بيانات الجهاز' data-trigger='hover'>"+
                "<button id='edit_devN' class='btn' data-toggle='modal' data-target='#EditDevice4CharModal'"+ "value='"+el.devId+","+el.charity_id+","+el.name+","+el.city+","+el.address+"'>"+
                "<i class='far fa-edit'  style='color: #fff;'></i>"+
                "</button>"+
                "</span>"+

                "<span class='d-inline-block' data-toggle='popover' data-trigger='hover' data-placement='top' data-content=' إحصائيات الجهاز' data-trigger='hover'>"+
                "<button  id='statistics_dev' class='btn'"+ "value='"+el.devId+"'>"+
                "<i class='fas fa-signal'  style='color: #fff;'></i>"+
                "</button>"+

                "</span>"+
                "<p class='text-right arabic-text'  style='margin-bottom: 0;'>"+
                "<span>"+ el.name+"</span>"+"<span class='arabic-text' style='margin-left: 20px;margin-right: 20px;'>اسم الجهاز</span>"+
                "</p>"+
                "<p class='text-right arabic-text'  style='margin-bottom: 0;'>"+
                "<span>"+ el.Device_serial+"</span>"+"<span class='arabic-text' style='margin-left: 20px;margin-right: 20px;'>رقم الجهاز</span>"+
                "</p>"+
                "<p class='text-right arabic-text' style='margin-bottom: 0;'>"+
                "<span class='arabic-text' style='margin-left: 20px;margin-right: 20px;'>الولاية</span><span>"+ el.city+"</span>"+
                "</p>"+
                "<p class='text-right arabic-text' style='margin-bottom: 0;'>"+
                "<span class='arabic-text' style='margin-left: 20px;margin-right: 20px;'>العنوان</span><span>"+ el.address+"</span>"+
                "</p>"+
                "<p class='text-right arabic-text'  style='margin-bottom: 0;'>"+
                "<span>"+ el.start_date+"</span>"+"<span class='arabic-text' style='margin-left: 20px;margin-right: 20px;'>تاريخ البدء  </span>"+
                "</p>"+
                "<p class='text-right arabic-text'  style='margin-bottom: 0;'>"+
                "<span>"+ el.last_maintenance+"</span>"+"<span class='arabic-text' style='margin-left: 20px;margin-right: 20px;'>تاريخ الصيانة  </span>"+
                "</p>"+
                "<p class='text-right arabic-text'  style='margin-bottom: 0;'>"+
                "<span>"+ el.next_maintenance+"</span>"+"<span class='arabic-text' style='margin-left: 20px;margin-right: 20px;'>تاريخ الصيانة القادم  </span>"+
                "</p>"+
                "<p class='text-right arabic-text'  style='margin-bottom: 0;'>"+
                "<span>"+ el.num_of_trans+"</span>"+"<span class='arabic-text' style='margin-left: 20px;margin-right: 20px;'>عدد التبرعات</span>"+
                "</p>"+
                "<p class='text-right arabic-text'  style='margin-bottom: 0;'>"+
                "<span>"+ el.sum+"</span>"+"<span class='arabic-text' style='margin-left: 20px;margin-right: 20px;'>مجموع التبرعات</span>"+
                "</p>"+
                "</div>"+"</div>"
                });
            }
               
        }});

});

//Edit subzakah type 
$(document).on('click', '#statistics_dev', function(){
    var Device_ID = $(this).val();
    console.log('Device_ID',Device_ID)
    var url = "devstatistics/?Device_ID=" + Device_ID
    $.ajax({
        type: "GET",
        url: "devstatistics",
        // Use "POST" method to send data
        data: {
            "Device_ID": Device_ID // Replace with your data
        },
        success: function(response){ 
            window.location.href = url;
    }
  //ajax 
   });
   
});


$(document).on('click', '#search2dates4oneDev', function(){
    var eDate = $('#filterDatetwo4dev').val();
    var sDate = $("#filterDateone4dev").val();
    var devID = $("#devID").val();
    var div =  document.getElementById('filterresponse'); 
    var url = "/dashboard/devstatistics/?Device_ID=" + devID
    console.log('sDate',sDate);
    if( $('#filterDatetwo4dev').val() == ''){$('#alert-ondevdatetwo').css("display","block");}
    if( $('#filterDateone4dev').val() == ''){$('#alert-ondevdateone').css("display","block");}
    if( $('#filterDatetwo4dev').val().length > 0 && $('#filterDateone4dev').val().length >0 ){
    // Create an object with the data to be sent
    var data = {
      'sDate': sDate,
      'eDate':eDate,
      'devID':devID
      
    };
    console.log('sDate',data);
    // Send an AJAX POST request to the Django view
    $.ajax({
      url: url,
      type: 'POST',
      data: data,
      success: function(response) {
        if(response.filter_num && response.filter_sum ){
        div.innerHTML+=
        "<div class='alert alert-success text-right arabic-text' role='alert'>"+
        "<span class='arabic-text'>عدد التبرعات</span>"+
        "<span class='arabic-text between2Dates_num px-1'>"+response.filter_num+"</span>"+
        "<span class='arabic-text'>مجموع التبرعات</span>"+
        "<span class='arabic-text between2Dates_numSum'>"+response.filter_sum+"</span>"+
        "</div>"
    }else{
        div.innerHTML+=
        "<div class='alert alert-danger  text-right arabic-text' role='alert'>"+
        "<span class='arabic-text'>لا توجد تبرعات</span>"+
        "</div>"
    }
        // Handle the response from the Django view
        console.log(response.filter_num);
        // Perform any additional actions or update the page as needed
      },
      error: function(error) {
        // Handle any errors that occur during the AJAX request
        console.log(error);
      }
    });
}
  });
$(document).on('click', '#close-datebtn4onedev', function(){
    $('#filterresponse').empty();
    $('#alert-ondevdatetwo').css("display","none");
    $('#alert-ondevdateone').css("display","none");
    $('#filterDatetwo4dev').val('') ;
    $("#filterDateone4dev").val('');

});

//filter with month 4 one device
$(document).on('click', '#search-month4onedev', function(){
    if ($('#gMonth4dev option:selected').val().length > 0){
        var month = $('#gMonth4dev').val();
        console.log("month",month);
    }
    if ($('#yearSelect4Dev option:selected').val().length > 0){
        var year = $('#yearSelect4Dev').val();
        console.log("year",year);
    }
    var devID = $("#devID4month").val();
    var div =  document.getElementById('filterresponse4month'); 
    var url = "/dashboard/devstatistics/?Device_ID=" + devID

    if( $('#gMonth4dev').val() === '' || $('#yearSelect4Dev').val() === ''){$('#alert-monthfilter4_Dev').css("display","block");}
    if( $('#gMonth4dev').val().length > 0 && $('#yearSelect4Dev').val().length >0 ){
    // Create an object with the data to be sent
    var data = {
      'month': month,
      'year':year,
      'devID':devID
      
    };
    console.log('data',data);
    // Send an AJAX POST request to the Django view
    $.ajax({
      url: url,
      type: 'POST',
      data: data,
      success: function(response) {
        if(response.filter_num && response.filter_sum ){
        div.innerHTML+=
        "<div class='alert alert-success text-right arabic-text' role='alert'>"+
        "<span class='arabic-text'>عدد التبرعات</span>"+
        "<span class='arabic-text between2Dates_num px-1'>"+response.filter_num+"</span>"+
        "<span class='arabic-text'>مجموع التبرعات</span>"+
        "<span class='arabic-text between2Dates_numSum'>"+response.filter_sum+"</span>"+
        "</div>"
    }else{
        div.innerHTML+=
        "<div class='alert alert-danger  text-right arabic-text' role='alert'>"+
        "<span class='arabic-text'>لا توجد تبرعات</span>"+
        "</div>"
    }
        // Handle the response from the Django view
        console.log(response.filter_num);
        // Perform any additional actions or update the page as needed
      },
      error: function(error) {
        // Handle any errors that occur during the AJAX request
        console.log(error);
      }
    });
}
  });
  $(document).on('click', '#close-monthYearbtn4onedev', function(){
    $('#filterresponse4month').empty();
    $('#alert-monthfilter4_Dev').css("display","none");
    $('#gMonth4dev').val('') ;
    $("#yearSelect4Dev").val('');

});
//Edit subzakah type 
$(document).on('click', '.edit_zsub', function(){

    var Eidit_Zakah_name = $(this).val();
    const splitParts = Eidit_Zakah_name.split(",");
    const arabicName = splitParts.length - 1;
    const englishName = splitParts.length - 2;
    console.log('Eidit_Zakah_name',Eidit_Zakah_name,'arabicName',arabicName,'englishName',englishName)
    $('#seteditsubval').val(Eidit_Zakah_name)
    $('input[name="subzar"]').val(splitParts[arabicName]);
    $('input[name="subzen"]').val(splitParts[englishName]); 
});

//validate edit subzakah form
$('#editsubz_form').on('submit', function(event) {
    // validateForm(event);
    event.preventDefault();
    var form = $(this);
    $.post(form.attr('action'), form.serialize(), function(response) {
        console.log(response)
        if(response == 'exit'){
            $('#alert-Edit_szakah_ar').css("display","none");       
            $('#alert-Eidit_szakah_en').css("display","none"); 
            $('#alert-Eidit_szakah_exit').css("display","block");
         
        }else if(response == 'empty'){
            $('#alert-Edit_szakah_ar').css("display","block");       
            $('#alert-Eidit_szakah_en').css("display","block"); 
            // $('#alert-Eidit_szakah_exit').css("display","none"); 
            // $('input[name="subzar"]').val("");
            // $('input[name="subzen"]').val(""); 
            // $('#Eidit_close-suzakah_type').click()
        }else{
            $('#alert-Edit_szakah_ar').css("display","none");       
            $('#alert-Eidit_szakah_en').css("display","none"); 
            $('#alert-Eidit_szakah_exit').css("display","none"); 
            $('input[name="subzar"]').val("");
            $('input[name="subzen"]').val(""); 
            $('#Eidit_close-suzakah_type').click()
            window.location.reload()
        }
  
           
        
    });

});
$('#Eidit_close-suzakah_type').click(function(e){ 
    if (e.target) {
    $('#alert-Edit_szakah_ar').css("display","none");       
    $('#alert-Eidit_szakah_en').css("display","none"); 
    $('#alert-Eidit_szakah_exit').css("display","none"); 
    $('input[name="subzar"]').val("");
    $('input[name="subzen"]').val("");  
    }
});


$(document).on('click', '#addsubzfortype', function() {
    var zakahId = $(this).val();
    console.log('zakahId',zakahId)
    $('input[name="zakahnameinurl"]').val(zakahId);  
 
  });

//validate add subzakah for special type 
$('#addsubz_form').on('submit', function(event) {
    // validateForm(event);
    event.preventDefault();
    var form = $(this);
    $.post(form.attr('action'), form.serialize(), function(response) {
        console.log(response)
        if(response == 'exit'){
            $('#warning-zakah_ar').css("display","none");       
            $('#warning-zakah_en').css("display","none"); 
            $('#warning-addszakah_ex').css("display","block");
      
         
        }else if(response == 'empty'){
            $('#warning-zakah_ar').css("display","block");       
            $('#warning-zakah_en').css("display","block"); 
           
        }else{
            $('#warning-addszakah_ex').css("display","none");       
            $('#arning-zakah_en').css("display","none"); 
            $('#aarning-zakah_ar').css("display","none"); 
            $('input[name="subar4type"]').val("");
            $('input[name="ssuben4type"]').val(""); 
            $('#closeaddszakah').click()
            window.location.reload()
        }
  
           
        
    });

});

$('#close-aszakah').click(function(e){ 
    if (e.target) {
        $('#warning-addszakah_ex').css("display","none");       
        $('#warning-zakah_en').css("display","none"); 
        $('#warning-zakah_ar').css("display","none"); 
        $('input[name="subar4type"]').val("");
        $('input[name="suben4type"]').val("");  
    }
});


//ADD subzakah for charity
    $(document).on('click','#szakah4charity', function(){
        var zakahName = $(this).val();
        console.log('zakahName',zakahName);       
        let modal_body = document.getElementById('subz4charadd');
        //Display message to user if press delete button
        //with an OK and a Cancel button
            $.ajax({
                type: "GET",
                url: "addsub",
                data: {
                'zakahName':zakahName
                },
                 success: function(response){
                    console.log(response);   
                    const obj = response.choose_subtypes;
                    console.log(typeof(obj))
                    if (obj.length == 0) {

                        if (modal_body.innerHTML.trim() == "") {
                            modal_body.innerHTML +=
                            "<div class='col-md-12 d-flex justify-content-center'>"+
                            "<h6 class='text-center arabic-text'>تم إضافة كل أنواع الصدقة الفرعية   </h6>"+
                            "</div>";
                        

                        }
          
                    }else{
                    // console.log(obj); 
                    if (modal_body.innerHTML.trim() == "") {
                        //do something
                    obj.forEach(el => {
                        modal_body.innerHTML+=
                       
                        " <div class='col-md-4'>"+
                            "<section class='app text-center'>"+
                                "<article class='feature1' id='mysubDiv'>"+
                                "<input type='checkbox' id='feature1' name='zakah'"+ "value='"+el.sub_type_en+":"+el.sub_type_ar+"'/>"+
                                "<div>"+
                                    "<span>"+
                                   "<p class='english-text' style='margin-bottom: 0;'>"+el.sub_type_en+"</p>"+
                                    "<p class='arabic-text' style='margin-bottom: 0;'>"+el.sub_type_ar+"</p>"+
                                    "</span>"+
                                "</div>"+
                                "</article>"+
                            "</section>"+
                            "</div>"
                        
                    });
               //if
             }}
        //Sucess    
             }

           //ajax 
            });
               //save checkedbox value in array
               $('#Addchazakah').on('click', function() {

                var myCheckboxes = new Array();
                
                $('[name="zakah"]').each(function(i,e) {
                    if ($(e).is(':checked')) {
                        myCheckboxes.push($(this).val());
                    }
                });
                
                console.log(myCheckboxes);
                const myJSON = JSON.stringify(myCheckboxes);
                console.log(myJSON);
                $.ajax({
                    type: "GET",
                    url: "addsub",
                    data: {
                      'myCheckboxes': myJSON,
                      'zakahName':zakahName
                    },
                    success: function(){
                    $("#close-chsubzakah").click();
                    window.location.reload(); 
                }});
                
             });
             $('#close-chsubzakah').click(function(e){ 
                if (e.target) {
                    modal_body.innerHTML = '';
                }
            });
    

            $('#Addotherchasubzakah').click(function(e){  
                if (e.target) {
                    console.log()
                    $('#setothersubzakah').val(zakahName)

                }
        
            });
        });

    $('#Addotherchasubzakah').click(function(e){  
        if (e.target) {
            $("#close-chsubzakah").click();
        }

    });
 
 //validate add other sub zakah 4 charity
 //validate add subzakah for special type 
$('#addothersubz_form').on('submit', function(event) {
    // validateForm(event);
    event.preventDefault();
    var form = $(this);
    $.post(form.attr('action'), form.serialize(), function(response) {
        console.log(response)
        if(response == 'exit'){
            $('#otheralert-subtype4charar').css("display","none");       
            $('#otheralert-subtype4charen').css("display","none");  
            $('#otheralertexit-subtype4char').css("display","block");
      
         
        }else if(response == 'empty'){
            $('#otheralert-subtype4charar').css("display","block");       
            $('#otheralert-subtype4charen').css("display","block"); 
           
        }else if(response == 'add'){{
            $('#otheralert-subtype4charar').css("display","none");       
            $('#otheralert-subtype4charen').css("display","none");  
            $('#otheralertexit-subtype4char').css("display","none");
            $('input[name="othersub4charar"]').val("");
            $('input[name="othersub4charen"]').val(""); 
            $('#closeothersubzakah4char').click()
            window.location.reload()
        }
  
           
        
    }});

});

$('#close-otherszakah4ch').click(function(e){ 
    if (e.target) {
        $('#otheralert-subtype4charar').css("display","none");       
        $('#otheralert-subtype4charen').css("display","none");  
        $('#otheralertexit-subtype4char').css("display","none");
        $('input[name="othersub4charar"]').val("");
        $('input[name="othersub4charen"]').val(""); 
}});   

//edit subzakah 4 charity 4 special type 

$(document).on('click', '.edit_zsub4char', function(){

    var Eidit_Zakah_name = $(this).val();
    const splitParts = Eidit_Zakah_name.split(",");
    const arabicName = splitParts.length - 1;
    const englishName = splitParts.length - 2;
    console.log('Eidit_Zakah_name',Eidit_Zakah_name)
    $('#seteditsubval4char').val(Eidit_Zakah_name)
    $('input[name="editsubzar4ch"]').val(splitParts[arabicName]);
    $('input[name="editsubzen4ch"]').val(splitParts[englishName]); 
});


//validate form 4 edit subzakah 4 type in charity
$('#editsub4type4char_form').on('submit', function(event) {
    // validateForm(event);
    event.preventDefault();
    var form = $(this);
    $.post(form.attr('action'), form.serialize(), function(response) {
        console.log(response)
        if(response == 'exit'){
            $('#warning-Edit_szakah_ar4char').css("display","none");       
            $('#warning-Eidit_szakah_en4char').css("display","none");  
            $('#warning-Eidit_szakah_exit4ch').css("display","block");
      
         
        }else if(response == 'empty'){
            $('#warning-Edit_szakah_ar4char').css("display","block");       
            $('#warning-Eidit_szakah_en4char').css("display","block");  
            $('#warning-Eidit_szakah_exit4ch').css("display","none");

           
        }else {
            $('#warning-Edit_szakah_ar4char').css("display","none");       
            $('#warning-Eidit_szakah_en4char').css("display","none");  
            $('#warning-Eidit_szakah_exit4ch').css("display","none");
            $('input[name="editsubzen4ch"]').val("");
            $('input[name="editsubzar4ch"]').val(""); 
            $('#Eidit_close-suzakah_type4char').click()
            window.location.reload()
        }

    });

});

$('#Eidit_close-suzakah_type4char').click(function(e){ 
    if (e.target) {
        $('#warning-Edit_szakah_ar4char').css("display","none");       
        $('#warning-Edit_szakah_en4char').css("display","none");  
        $('#warning-Eidit_szakah_exit4ch').css("display","none");
        $('input[name="editsubzen4ch"]').val("");
        $('input[name="editsubzar4ch"]').val(""); 
}}); 

//add subzakah 4 type 4 charity

$(document).on('click', '#addsubz4type4char', function() {
    var zakahName = $(this).val();
    console.log('addsubz4type4char click', zakahName);
    $('input[name="zakahnameurl"]').val(zakahName);  
  })

//validate form 4 add subzakah 4 type in charity
$('#addsubzfortype4char_form').on('submit', function(event) {
    // validateForm(event);
    event.preventDefault();
    var form = $(this);
    $.post(form.attr('action'), form.serialize(), function(response) {
        console.log(response)
        if(response == 'exit'){
            $('#warningadd-subzakah_ar4typeChar').css("display","none");       
            $('#warningadd-subzakah_en4typeChar').css("display","none");  
            $('#warningadd-subzakah_ex4typeChar').css("display","block");
      
        }else if(response == 'empty'){
            $('#warningadd-subzakah_ar4typeChar').css("display","block");       
            $('#warningadd-subzakah_en4typeChar').css("display","block");  
            $('#warningadd-subzakah_ex4typeChar').css("display","none");

           
        }else {
            $('#warningadd-subzakah_ar4typeChar').css("display","none");       
            $('#warningadd-subzakah_en4typeChar').css("display","none");  
            $('#warningadd-subzakah_ex4typeChar').css("display","none");
            $('input[name="suben4type4charity"]').val("");
            $('input[name="subar4type4charity"]').val(""); 
            $('#close-aszakah4chartype').click()
            window.location.reload()
        }

    });

});

$('#close-aszakah4chartype').click(function(e){ 
    if (e.target) {
        $('#warningadd-subzakah_ar4typeChar').css("display","none");       
        $('#warningadd-subzakah_en4typeChar').css("display","none");  
        $('#warningadd-subzakah_ex4typeChar').css("display","none");
        $('input[name="suben4type4charity"]').val("");
        $('input[name="subar4type4charity"]').val(""); 
}}); 



$('.visitUrl').click(function() {
    var valueToSend = $(this).val();
    $('input[name="name"]').val(valueToSend);
 
  });


  $(document).on('click', '.ViewSub_zaka4admin', function() {
    var zakahId = $(this).val();
    console.log('zakahId',zakahId)
    $('#zakahId').val(zakahId);
    $('#Form2sendid').submit();
  });
});//Ready document Jquery function 