
function Day(name) {
    this.name = ko.observable(name);
    this.guests = ko.observableArray([]);
}

function Guest(data) {
    this.name = ko.observable(data.name);
    this.id = ko.observable(data.id);
}

function DateModel(offsetFromToday) {
    var that = this;
    var date = new Date();
    date.setDate(new Date().getDate() + offsetFromToday);
    this.value = ko.observable(date);

    this.text = ko.pureComputed({
        read: function() {
            return formatDate(that.value());
        },
        write: function(value) {
            var withYear = Date.parse(value + ", " + new Date().getFullYear());
            that.value(withYear);
        }
    });
}

function WeekPlan() {
    var that = this;
    this.fromDate = ko.observable(new DateModel(+1));
    this.toDate = ko.observable(new DateModel(+7));

    this.days = ko.computed(function() {
        var days = [];
        var date = that.fromDate().value();
        while (date < that.toDate().value()) {
            days.push(new Day(formatDate(date)));
            date.setDate(date.getDate() + 1);
        }
        return days;
    });

//    this.invite = function(dayIndex, personIndex) {
//        this.days[dayIndex].guests.push(self.people[personIndex])
//    }

    this.people = ko.observableArray([]);
    var guests = console.debug(document.getElementById('guests-data').textContent);
    console.debug(guests);
    for (g in guests) {
        this.people.push(new Guest(g));
    }
    console.debug(guests);
}
