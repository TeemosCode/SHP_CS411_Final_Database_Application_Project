/* Style Changer */

jQuery(document).ready(function($){
	if($('body').hasClass('stretched-layout')){
		$('#layout').val('stretched');
	} else {
		$('#layout').val('boxed');
	}
	
	$('.handler').click(function(){
		if ($(this).hasClass('closed')){
			$(this).next('.options').parent().animate({left:0}, 300, function(){
				$(this).find('.handler').removeClass('closed');
			});
		} else {
			$(this).parent().animate({left:'-152px'}, 300, function(){
				$(this).find('.handler').addClass('closed');
			});
		}
		return false;
	});
	
	$('.handler').parent().delay(1000).animate({left:'-152px'}, 300, function(){
		$(this).find('.handler').addClass('closed');
	});
	
	// layout
	if ( $('#layout').val() == 'stretched' )
	   $('#bgs').hide();
	$('#layout').change(function(){
	    var layout = $(this).val();
        $('body').removeClass('boxed-layout stretched-layout').addClass( $(this).val() + '-layout' );
        if ( layout == 'boxed' ) {
			$('#layout').val('boxed');
            $('#bgs').slideDown(200);   
	        $('body').css({backgroundColor:'#' + $('#stlChanger').find('#bgColor').attr('title')});
        } else {
			$('#layout').val('stretched');
            $('#bgs').slideUp(200);   
            if ( $('.stretched-layout .bgWrapper').length > 0 )  
	           $('.stretched-layout .bgWrapper').css({'background':'#fff'});
	        else if ( $('.stretched-layout .wrapper').length > 0)
	           $('.stretched-layout .wrapper').css({'background':'#fff'});
        }

	});
	
	// headings font
	$('#hfont').change(function(){
        var selectors = 'h1, h2, h3, h4, h5, h6, .special-font, #slogan h1';
		var maya = '.theme-maya #sidebar .widget h2, .theme-maya #sidebar .widget h3, .theme-maya #footer .widget h2, .theme-maya #footer .widget h3, .theme-maya .short-text, .theme-maya h2.post-title a';
        var gFontVal = $("option:selected", this).val();
		var gFontName = gFontVal.split(':');
		if ($('head').find('link#gFontName').length < 1){
			$('head').append('<link id="gFontName" rel="stylesheet" type="text/css" href="" />');
		}
		if ($('head').find('style#gFontStyles').length < 1){
			$('head').append('<style id="gFontStyles" type="text/css"></style>');
		}
		$('link#gFontName').attr({href:'http://fonts.googleapis.com/css?family=' + gFontVal});
		$('style#gFontStyles').html(selectors + ', ' + maya + ' { font-family:"' + gFontName[0] + '", "Trebuchet MS", Arial, "Helvetica CY", "Nimbus Sans L", sans-serif !important; }');
	});
	
	// logo font
	$('#logoFont').change(function(){
        var selectors = '#logo .logo-title, .logo';
        var gFontVal = $("option:selected", this).val();
		var gFontName = gFontVal.split(':');
		if ($('head').find('link#logoFontName').length < 1){
			$('head').append('<link id="logoFontName" rel="stylesheet" type="text/css" href="" />');
		}
		if ($('head').find('style#logoFontStyles').length < 1){
			$('head').append('<style id="logoFontStyles" type="text/css"></style>');
		}
		$('link#logoFontName').attr({href:'http://fonts.googleapis.com/css?family=' + gFontVal});
		$('style#logoFontStyles').html(selectors+' { font-family:"' + gFontName[0] + '", "Trebuchet MS", Arial, "Helvetica CY", "Nimbus Sans L", sans-serif !important; }');
	});
	
	// paragraph
	$('#pfont').change(function(){
		var pfontVal = $("#pfont option:selected").val();
		if ($('head').find('style#cFontStyles').length < 1){
			$('head').append('<style id="cFontStyles" type="text/css"></style>');
		}
		$('style#cFontStyles').text('body, p, blockquote, li, small { font-family:' + pfontVal + ' !important; }');
	});
	
	// colorpicker body background      
	$('.style-picker #bgColor').parent('a').ColorPicker({
		onChange:function(hsb, hex, rgb){
			$('.style-picker').find('#bgColor').css({backgroundColor:'#' + hex});
			$('body').css({backgroundColor:'#' + hex});
		},
		onSubmit:function(hsb, hex, rgb, el){
			$(el).find('#bgColor').css({backgroundColor:'#' + hex});
			$(el).find('#bgColor').attr({title:hex});
			$('body').css({backgroundColor:'#' + hex});
			$(el).ColorPickerHide();
		},
		onBeforeShow:function(){
		    var hex = $('.style-picker').find('#bgColor').attr('title');
			$(this).ColorPickerSetColor(hex); 
		}
	});
	
	// change header bg
	$('.style-picker a.bgHeader').click(function(){
        var imgUrl = $(this).attr('href');
        $('#header').css({'background-image':"url('"+imgUrl+"')"});
        return false;
    });
	
	// change body bg
	$('.style-picker a.bgBody').click(function(){
        var imgUrl = $(this).attr('rel');
        $('body').css({'background-image':"url('"+imgUrl+"')", "background-attachment":"fixed", "background-position":"top center", "background-attachment":"fixed", "background-repeat":"repeat"});
        return false;
    });
});