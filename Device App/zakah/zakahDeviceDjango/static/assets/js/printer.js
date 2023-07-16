
// $.getScript("bxlpos.js", function() {
 //    $.getScript("bxllabel.js", function() {
//         $.getScript("bxlcommon.js", function() {


	var LF = "\n";
	var issueID = 1;
	var tmp = "123456789"
	var _inch = 3;

    function data(a, b) {
        var result = 0;
        result = a + b;
        return result;
    }

	function changeInch() {
		_inch = type_inch.value;
	}

	function viewResult(result) {
		// p_result.value = result;
	}

    function PrintReceipt_ar(value) {

        // if (value == 0) return false;

        var name = "Dar Ata'a";

		setPosId(issueID);
		checkPrinterStatus();

		printText("إيصال التبرع\n\n", 0, 0, false, false, false, 0, 1);

			printText("--------------------------------\n", 0, 0, false, false, false, 0, 0);
            // printText("                             " + name + " : اسم الجمعية \n", 0, 1, true, false, false, 0, 0);
            // printText("                             " + id    + " : رقم التبرع \n", 0, 1, true, false, false, 0, 0);
            // printText("                             " + type  + " : نوع التبرع \n", 0, 1, true, false, false, 0, 0);
            printText("                 ريال عماني  " + value + " :      المبلغ \n", 0, 1, true, false, false, 0, 0);
			printText("--------------------------------\n", 0, 0, false, false, false, 0, 0);
// Dar Ata'a
        printText(name + "\n", 0, 0, true, false, false, 0, 0);
		printText("Tel : +968 24222885\n", 0, 0, true, false, false, 0, 0);
	//	printText("Homepage : www.daralatta.org\n", 0, 0, false, false, false, 0, 0);

	//	printQRCode("www.daralatta.org",0,1,7,0);
		printText("\n\n", 0, 0, false, false, false, 0, 0);
		cutPaper(0);

		var strSubmit = getPosData();

		console.log(strSubmit);

		issueID++;
		// requestPrint(p_name.value, strSubmit, viewResult);
		requestPrint("Printer1", strSubmit, viewResult);

		return true;
	}

	function PrintReceipt(name, value, tr_id , type, phone, web, datetime) {

        // if (value == 0) return false;
        // var name = "dar ata'a";
		setPosId(issueID);
		checkPrinterStatus();

		printText("\n\nYour Donation Receipt\n\n", 0, 0, false, false, false, 0, 1);

			       printText("--------------------------------\n", 0, 0, false, false, false, 0, 0);
                   printText("    Donation Date   " + datetime + "\n", 0, 0, true, false, false, 0, 0);
 if (tr_id!="")    printText("    Donation ID     " + tr_id + "\n", 0, 0, true, false, false, 0, 0);
 if (type!="")     printText("    Donation type   " + type + "\n", 0, 0, true, false, false, 0, 0);
                   printText("    Total           " + value + "  OMR\n", 0, 0, true, false, false, 0, 0);
			       printText("--------------------------------\n", 0, 0, false, false, false, 0, 0);

        printText(name + "\n", 0, 0, true, false, false, 0, 0);
		if (phone!="") printText("Tel : +968 " + phone +"\n", 0, 0, true, false, false, 0, 0);
		if (web!="")   printText("Homepage : " + web +"\n", 0, 0, false, false, false, 0, 0);

		if (web!="")   printQRCode(web,0,1,7,0);
		else if (phone!="")  printQRCode("+968" + phone,0,1,7,0);
		printText("\n\n\n\n", 0, 0, false, false, false, 0, 0);
		cutPaper(0);

		var strSubmit = getPosData();
		console.log(strSubmit);

		issueID++;
		// requestPrint(p_name.value, strSubmit, viewResult);
		requestPrint("Printer1", strSubmit, viewResult);

		return true;
	}


	var arrSymbol = [0, 1, 2, 3, 5, 6, 4, 7, 8];

	function PrintBarcode() {
		var barCodeData = barcode_data.value;
		var barCodeSymbol = arrSymbol[b_symbol.selectedIndex];
		var barCodeHeight = 100;
		var barCodeWidth = 3;

		var barCodeAlignment = b_align.selectedIndex;
		var barCodeHri = print_HRI.selectedIndex;

		setPosId(issueID);

		printText("print1DBarcode\n\n", 0, 0, false, false, false, 0, 0);
		print1DBarcode(barCodeData, barCodeSymbol, barCodeWidth, barCodeHeight, barCodeHri, barCodeAlignment);
		printText("\n\n\n\n\n\n\n\n", 0, 0, false, false, false, 0, 0);

		cutPaper();

		var strSubmit = getPosData();

		console.log(strSubmit);

		issueID++;
		requestPrint(p_name.value, strSubmit, viewResult);
	}

	function PrintPagemode() {

		var rotation = pagemode_direct.selectedIndex;

		setPosId(issueID);

		checkPrinterStatus();
		pagemodeBegin();
		pagemodePrintArea(512, 700);
		pagemodePrintDirection(rotation);

		if (pagemode_direct.selectedIndex == 0) {//Normal
			pagemodePrintPosition(0, 80);
			printText("mPrint Server!\n", 0, 1, false, false, false, 0, 0);
			pagemodePrintPosition(0, 150);
			printText("Test Print!!\n", 0, 0, false, false, false, 0, 0);
			pagemodePrintPosition(0, 230);
			printText(pagemode_direct.value, 0, 0, false, false, false, 0, 0);
			pagemodePrintPosition(100, 350);
			printQRCode("http://www.bixolon.com", 0, 0, 5, 0);
		} else if(pagemode_direct.selectedIndex == 1 || pagemode_direct.selectedIndex == 3) {  //Left90 or Right90
			pagemodePrintPosition(100, 100);
			printText("mPrint Server\n", 0, 1, false, false, false, 0, 0);
			pagemodePrintPosition(100, 170);
			printText("Test Print!!\n", 0, 0, false, false, false, 0, 0);
			pagemodePrintPosition(100, 250);
			printText(pagemode_direct.value, 0, 0, false, false, false, 0, 0);
			pagemodePrintPosition(200, 350);
			printQRCode("http://www.bixolon.com", 0, 0, 5, 0);
		}
		else{//Rotate180
			pagemodePrintPosition(100, 100);
			printText("mPrint Server!\n", 0, 1, false, false, false, 0, 0);
			pagemodePrintPosition(100, 170);
			printText("Test Print!!\n", 0, 0, false, false, false, 0, 0);
			pagemodePrintPosition(100, 250);
			printText(pagemode_direct.value, 0, 0, false, false, false, 0, 0);
			pagemodePrintPosition(230, 350);
			printQRCode("http://www.bixolon.com", 0, 0, 5, 0);

		}
		pagemodeEnd();
		printText("\n\n\n\n\n", 0, 0, false, false, false, 0, 0);
		cutPaper();
		console.log(strSubmit);

		var strSubmit = getPosData();

		issueID++;
		requestPrint(p_name.value, strSubmit, viewResult);
	}

	function erase() {
		var sigCanvas = document.getElementById("canvas");
			var context = sigCanvas.getContext("2d");
			context.clearRect(0, 0, sigCanvas.width, sigCanvas.height);
	}

	// works out the X, Y position of the click inside the canvas from the X, Y position on the page
	function getPosition(mouseEvent, sigCanvas) {
		var rect = sigCanvas.getBoundingClientRect();
		return {
			X: mouseEvent.clientX - rect.left,
			Y: mouseEvent.clientY - rect.top
		};
	}

	function initialize() {
		// get references to the canvas element as well as the 2D drawing context
		var sigCanvas = document.getElementById("canvas");
		var context = sigCanvas.getContext("2d");
		context.strokeStyle = "#FF";
		context.lineJoin = "round";
		context.lineWidth = 5;


		// This will be defined on a TOUCH device such as iPad or Android, etc.
		var is_touch_device = "ontouchstart" in document.documentElement;

		if (is_touch_device) {
			// create a drawer which tracks touch movements
			var drawer = {
				isDrawing: false,
				touchstart: function (coors) {
					context.beginPath();
					context.moveTo(coors.x, coors.y);
					this.isDrawing = true;
				},
				touchmove: function (coors) {
					if (this.isDrawing) {
						context.lineTo(coors.x, coors.y);
						context.stroke();
					}
				},
				touchend: function (coors) {
					if (this.isDrawing) {
						this.touchmove(coors);
						this.isDrawing = false;
					}
				}
			};

			// create a function to pass touch events and coordinates to drawer
			function draw(event) {
				// get the touch coordinates.  Using the first touch in case of multi-touch
				var coors = {
					x: event.targetTouches[0].pageX,
					y: event.targetTouches[0].pageY
				};

				// Now we need to get the offset of the canvas location
				var obj = sigCanvas;

				if (obj.offsetParent) {
					// Every time we find a new object, we add its offsetLeft and offsetTop to curleft and curtop.
					do {
						coors.x -= obj.offsetLeft;
						coors.y -= obj.offsetTop;
					} while (
						// The while loop can be "while (obj = obj.offsetParent)" only, which does return null
						// when null is passed back, but that creates a warning in some editors (i.e. VS2010).
						(obj = obj.offsetParent) != null
					);
				}

				// pass the coordinates to the appropriate handler
				drawer[event.type](coors);
			}

			// attach the touchstart, touchmove, touchend event listeners.
			sigCanvas.addEventListener("touchstart", draw, false);
			sigCanvas.addEventListener("touchmove", draw, false);
			sigCanvas.addEventListener("touchend", draw, false);

			// prevent elastic scrolling
			sigCanvas.addEventListener(
				"touchmove",
				function (event) {
					event.preventDefault();
				},
				false
			);
		} else {
			// start drawing when the mousedown event fires, and attach handlers to
			// draw a line to wherever the mouse moves to
			$("#canvas").mousedown(function (mouseEvent) {
				var position = getPosition(mouseEvent, sigCanvas);
				context.moveTo(position.X, position.Y);
				context.beginPath();

				// attach event handlers
				$(this)
					.mousemove(function (mouseEvent) {
						drawLine(mouseEvent, sigCanvas, context);
					})
					.mouseup(function (mouseEvent) {
						finishDrawing(mouseEvent, sigCanvas, context);
					})
					.mouseout(function (mouseEvent) {
						finishDrawing(mouseEvent, sigCanvas, context);
					});
			});
		}
	}


	// draws a line to the x and y coordinates of the mouse event inside
	// the specified element using the specified context
	function drawLine(mouseEvent, sigCanvas, context) {
		var position = getPosition(mouseEvent, sigCanvas);

		context.lineTo(position.X, position.Y);
		context.stroke();
	}

//         });
//    });
// });