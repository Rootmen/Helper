(function(){
    const ATTR_GOBACK = 'menu-goback';

    var prevMenus = [];
    
    var curretMenu = $("#menu-main");

    $(".menuitem").click(
        function() {
            if(hasAttr($(this), 'data-menuId'))
            {
                var self = $(this);

                if(hasAttr($(this), 'data-auth')) {
                    $.get($(this).attr('data-auth'),
                        function(data) {
                            var arr = data.split("||", 2);
                            if(arr[0] == '1') {
                                //ok
                                selectMenu(self);
                            } else {
                                window.location.href = arr[1];
                            }
                        });

                } else {
                    selectMenu($(this));
                }
                
            }
        }
    );

    function selectMenu(sender) {
        if(sender.attr('data-menuId') == ATTR_GOBACK) {
            goBack();
        } else {
            prevMenus.push(curretMenu);
            curretMenu.hide();
            curretMenu = $('#' + sender.attr('data-menuId'));
            curretMenu.show();
        }
    }

    function goBack() {
        if(prevMenus.length > 0)
        {
            curretMenu.hide();
            curretMenu = prevMenus.pop();
            curretMenu.show();
        }
    }

    var additional = {
        "mathelp": '<div class="form-row"><div class="form-group col-md-12"><div class="input-group mb-2 mr-sm-2"><div class="input-group-prepend"><div class="input-group-text"><i class="far fa-comment"></i></div></div> <input type="text" class="form-control" name="typeconcession" placeholder="Категория (инвалид, сирота и др.)" /></div></div></div>',
        "mathelpHostel": '',
        "changeStudy": '<div class="form-row"><div class="form-group col-md-6"> Текущая форма обчения<div class="input-group mb-2 mr-sm-2"><div class="input-group-prepend"><div class="input-group-text"><i class="far fa-comment"></i></div></div> <select class="custom-select" name="for1" ><option value="1">Очная</option><option value="2">Заочная</option><option value="3">Очно-заочная</option> </select></div></div><div class="form-group col-md-6"> Форма обучения на которую вы хотите перевестись<div class="input-group mb-2 mr-sm-2"><div class="input-group-prepend"><div class="input-group-text"><i class="far fa-comment"></i></div></div> <select class="custom-select" name="for2" ><option value="1">Очная</option><option value="2">Заочная</option><option value="3">Очно-заочная</option> </select></div></div></div>',
    }

    $('.menuclaim').click(
        function() {
            setClaimType(additional[$(this).attr('data-addy')]);
            selectMenu($(this));
            
        }
    );

    function setClaimType(html) {
        $('#claim-additional').html(html);
    }

    function hasAttr(obj, attribute) {
        var attr = obj.attr(attribute);
        return typeof attr !== typeof undefined && attr !== false;
    }
})();