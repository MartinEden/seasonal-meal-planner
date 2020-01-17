function Diner(data) {
    this.dinerName = ko.observable(data.name);
    this.id = ko.observable(data.id);
}

/*var getDiner = function(name, id) {
    return {
        diner: new Diner({"name": name, "id": id}),
    };
};


   this.selectedPeopleIndices = ko.observable([])
   this.selectedPeople = ko.computed(function(){
     var peeps = []
     for (index in this.selectedPeopleIndicies)
     {
        peeps.push(that.people[index]);
        return peeps;
     }
   });


   */
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

function TagConstraint(data) {
    this.name = ko.observable(data.name)
    this.max = ko.observable(1)
    this.min = ko.observable(0)
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
    var allPeople = JSON.parse(document.getElementById('guests-data').textContent);
    for (p in allPeople) {
        this.people.push(new Diner(allPeople[p]));
    }

    this.tags = ko.observableArray();
    this.selectedOption = ko.observable();
    addConstraint = function(item) {
        var match = ko.utils.arrayFirst(that.tags,
            function(item) {
                return that.selectedOption.value === item.value;
            });
        //if (match. is not defined )){
        that.tags.push(that.selectedOption)
        //}
        console.debug(that.selectedOption)
    };

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