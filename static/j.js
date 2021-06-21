async function test(){

    var res = await fetch('http://127.0.0.1:5000/api')
    var data =  await res.json();
    console.log(data);

}

test();