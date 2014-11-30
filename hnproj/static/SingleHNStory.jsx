function monthToStr(month) {
  switch (month) {
    case 0:
      return "Jan"; break;
    case 1:
      return "Feb"; break;
    case 2:
      return "Mar"; break;
    case 3:
      return "Apr"; break;
    case 4:
      return "May"; break;
    case 5:
      return "June"; break;
    case 6:
      return "July"; break;
    case 7:
      return "Aug"; break;
    case 8:
      return "Sept"; break;
    case 9:
      return "Oct"; break;
    case 10:
      return "Nov"; break;
    case 11:
      return "Dec"; break;
  }
  return "";
}

SingleStory = React.createClass({
  render: function() {
    var url = this.props.story["url"];
    var time = this.props.story["time"] * 1000;
    var storyDate = new Date(time);
    var month = storyDate.getMonth();
    var datestr = monthToStr(month) + " " + storyDate.getDate() + ", " + storyDate.getFullYear();
    var user = "";
    if (this.props.showUser) {
      user = "<span className=\"username\">" + this.props.story["by"] + "</span>";
    return (
      <div className="singleStoryDiv">
        <a href={url}>{this.props.story["title"]}</a> <span className="score">({this.props.story.score})</span>  <span className="storyDate">{datestr}</span>{{user}}
      </div>
    );
  }
});
