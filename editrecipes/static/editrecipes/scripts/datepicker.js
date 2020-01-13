function setupDatePickers() {
	var dateFormat = "D, d M";
	$.datepicker.setDefaults(
		$.extend({
			'dateFormat': dateFormat
		}, )
	);
	var from = $("#from")
		.datepicker({
			showButtonPanel: true,
			minDate: 0,
			maxDate: "+1W",
			hideIfNoPrevNext: true
		})
		.on("change", function() {
			to.datepicker("option", "minDate", getDate(this));
		}),
		to = $("#to").datepicker({
			showButtonPanel: true,
			maxDate: "+2W",
			minDate: 0,
			hideIfNoPrevNext: true,
		})
		.on("change", function() {
			from.datepicker("option", "maxDate", getDate(this));
		});
}

function getDate(element) {
	var date;
	try {
		date = $.datepicker.parseDate(dateFormat, element.value);
	} catch (error) {
		date = null;
	}

	return date;
}

function formatDate(date) {
	return date.toLocaleDateString("en-GB", {
		weekday: 'short',
		day: 'numeric',
		month: 'short'
	});
}