class App extends React.Component{
constructor(props){
super(props);
this.state={content:[{id:1, profile:'Awwal', date:'2020', likes:[], comment:[], body:'hello boy'}, 
{id:2, profile:'Malik', date:'2020', likes:['awwal'] , comment:[], body:'Twitter is fun'}] 
}
}

async componentWillMount(){
var G=await fetch('http://127.0.0.1:8000/tweet/')
var M=await G.json()
console.log(M)
this.setState({content:M})
console.log(this.state)
}

render(){

return(

<div>
<div className='header'><span className='circle-header'></span><span className='username-header'>{this.props.user}</span>
<div class='left logo'><i class='fab fa-twitter'></i></div>
</div>
{this.state.content.map(function(x){return <Tweet id={x.id} user={x.profile} likes={x.likes} body={x.body} date={x.date} />})}
</div>

)
}
 }
 
 var count=0;
 
class Tweet extends React.Component{
constructor(props){
super(props);
this.state={likes:[], retweets:0, comments:[]}
this.count=0
}

addLike=()=>{
var che=document.getElementById(this.props.id)
var add=che.classList.add('liked')
var remove=che.classList.remove('liked')
this.count<=0 ? this.count=1: this.count=-1
this.count<=0 ? che.classList.remove('liked') : che.classList.add('liked')
//console.log(count)
var lk=this.state.likes+this.count
this.setState({likes:lk});
}

componentWillMount(){
this.setState({likes:this.props.likes.length})
}

render(){
return(
<div>
<div className='box '>
<table>
<tr>
<td class='image-space'>
<img class='avatar'/></td>
<td class='full'><b class='user'>{this.props.user}</b>
<span class='passive date'> .{this.props.date}</span>
<div class='body'>{this.props.body}</div>
<p className='seperate'>
<button onClick={this.addLike}><span className='sticker'><i id={this.props.id} class='fas fa-heart'></i></span> {this.state.likes}</button> 
<button><span className='sticker'><i class='fas fa-share'></i></span> {this.state.retweets}</button> 
<button><span className='sticker'><i class='fas fa-comment'></i></span> {this.state.comments.length}</button> </p>

</td>
</tr>
</table>

</div>
</div>
)
}

}
 
//var part=document.getElementById('body')
//ReactDOM.render(<App user='Awwal' />, part)
var part=document.getElementById('body')
//ReactDOM.render(<App user='{request.user}' />, part)

 //<div><span class='circle'>