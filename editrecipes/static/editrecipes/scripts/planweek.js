function Diner(data) {
    this.dinerName = ko.observable(data.name);
    this.id = ko.observable(data.id);
}

function Day(name) {
    var that = this;
    this.name = ko.observable(name);
    this.guests = ko.observableArray();

    this.latestGuest = ko.computed({
        read: function() {
            return this.guests().length ? this.guests()[this.guests().length - 1] : "";
        },
        write: function(value) {
            if (value) {
                if (this.guests.indexOf(value) == -1) {
                    this.guests.push(value);
                }
            } else {
                this.guests.pop();
            }
        },
        owner: this
    });

    this.removeGuest = function(guest) {
        var index = that.guests.indexOf(guest);
        that.guests.splice(index, 1);
    }
}

function DateModel(offsetFromToday) {
    var date = new Date();
    date.setDate(new Date().getDate() + offsetFromToday);
    this.value = ko.observable(date);

    this.text = ko.computed({
        read: function() {
            return formatDate(this.value());
        },
        write: function(value) {
            var withYear = Date.parse(value + ", " + new Date().getFullYear());
            this.value(new Date(withYear));
        },
        owner: this
    });
}

function TagConstraint(name, max, min) {
    this.name = ko.observable(name)
    this.max = ko.observable(max)
    this.min = ko.observable(min)
}

function WeekPlan() {
    this.fromDate = ko.observable(new DateModel(+1));
    this.toDate = ko.observable(new DateModel(+7));

    this.days = ko.computed({
        read: function() {
            var days = [];
            var date = this.fromDate().value();
            while (date < this.toDate().value()) {
                days.push(new Day(formatDate(date)));
                date.setDate(date.getDate() + 1);
            }
            return days;
        },
        owner: this
    });

    this.people = ko.observableArray([]);
    var allPeople = JSON.parse(document.getElementById('guests-data').textContent);
    for (p in allPeople) {
        this.people.push(new Diner(allPeople[p]));
    }

    var allTags = JSON.parse(document.getElementById('tags-data').textContent);
    this.maxTags = ko.observableArray();
    for (t in allTags) {
        this.maxTags.push(new TagConstraint(allTags[t],1,0));
    }
    this.chosenMaxTags = ko.observableArray();
    this.minTags = ko.observableArray();
    for (t in allTags) {
        this.minTags.push(new TagConstraint(allTags[t],0,1));
    }
    this.chosenMinTags = ko.observableArray();

    this.chosenTags = ko.computed({
        read: function () {
            return this.chosenMaxTags().concat(this.chosenMinTags());
        },
        owner: this
    });


//    addConstraint = function(item) {
//        var match = ko.utils.arrayFirst(that.tags,
//            function(item) {
//                return that.selectedOption.value === item.value;
//            });
//        //if (match. is not defined )){
//        this????.tags.push(that.selectedOption)
//        //}
//        console.debug(that.selectedOption)
//    };

    /*this.options = this.tags.map(function (element) {
        // JQuery.UI.AutoComplete expects label & value properties, but we can add our own
        return {
            label: element.name,
            value: element.id,
            // This way we still have access to the original object
            object: element
        };
    });*/


}