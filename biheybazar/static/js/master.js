// console.log('Hello world')

console.log("hello world")

// get stars

const one=document.getElementById('first')

const two=document.getElementById("second")

const three=document.getElementById("third")

const four=document.getElementById("fourth")

const five=document.getElementById("fifth")

const form= document.querySelector('form')
const confirmbox = document.getElementById('rate-it')
const csrf = document.getElementsByName('csrfmiddlewaretoken')
console.log(csrf)
const d = document.getElementById('desc')
// console.log(d.val())

// console.log(form)
// console.log(confirmbox)
// console.log(csrf)
// console.log(one)
// 
const handleStarSelect=(size)=>{
    const children = form.children

    for (let i=0; i<children.length; i++){
        if (i<=size){
            children[i].classList.add('checked')
        }else{
            children[i].classList.remove('checked')
        }
    }
}

// handleStarSelect(2)

const handleSelect=(selection)=>{
switch(selection){
    case 'first':{
        // one.classList.add('checked')
        // two.classList.remove('checked')
        // three.classList.remove('checked')
        // four.classList.remove('checked')
        // five.classList.remove('checked')
        handleStarSelect(1)
        return
    }
    case 'second':{
        handleStarSelect(2)
        return
    }
    case 'third':{
        handleStarSelect(3)
        return
    }
    case 'fourth':{
        handleStarSelect(4)
        return
    }
    case 'fifth':{
        handleStarSelect(5)
        return
    }
}

}

const getNumericValue =(stringvalue)=>{
    let numericValue;
    if (stringvalue=='first'){
        numericValue=1;
    }else if(stringvalue=='second'){
        numericValue=2;
    }
    else if(stringvalue=='third'){
        numericValue=3;
    }

    else if(stringvalue=='fourth'){
        numericValue=4;
    }

    else if(stringvalue=='fifth'){
        numericValue=5;
    }
    else{
        numericValue=0;
    }

    return numericValue
    


}




if(one){
const arr = [one, two, three , four, five]

arr.forEach(item=> item.addEventListener('mouseover',(event)=>{
    handleSelect(event.target.id)}))


    arr.forEach(item=> item.addEventListener('click',(event)=>{
        const val= event.target.id
        const val_num = getNumericValue(val)
        // console.log(val)
        console.log(val_num)

        form.addEventListener('submit',e=>{
            e.preventDefault()
            // const id = e.target.id
            console.log('in')

            const val_num = getNumericValue(val)
            const data = document.getElementById('inpt')
            // console.log(data)

            // $(function () {
            //     $('textarea').ckeditor();
            //     $('#inpt').on('click', function(e) {
            //         console.log('no')
            //       console.log('ckeditor content: ' + $('textarea').val());
            //     })
            //   });

            
            
            $.ajax({
                type:"POST",
                url:'',
                data:{
                    'csrfmiddlewaretoken': csrf[0].value,
                    'ratings':val_num,
                    'description':text
                },
                success:function (response){
                    console.log(response)
                    confirmbox.innerHTML='rated'
                    
                },
                error:function(error){
                    console.log(error)
                    confirmbox.innerHTML='error'
                }
               
            }
            
            )
        })

        }))
        }
        // $(document).on('submit', '#rate-form',function(e){
        //     const val_num = getNumericValue(val)
        //     $.ajax({
        //         type:'POST',
        //         url:'',
        //         data:{
        //             'csrfmiddlewaretoken': csrf[0].value,
        //             'ratings':val_num,
        //             'description':$('#desc').val()
        //             // action: 'post'
        //         },
        //         success:function(json){
        //             document.getElementById("post-form").reset();
        //             // $(".posts").prepend('<div class="col-md-6">'+
        //             //     '<div class="row no-gutters border rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-250 position-relative">' +
        //             //         '<div class="col p-4 d-flex flex-column position-static">' +
        //             //             '<h3 class="mb-0">' + json.title + '</h3>' +
        //             //             '<p class="mb-auto">' + json.description + '</p>' +
        //             //         '</div>' +
        //             //     '</div>' +
        //             // '</div>' 
        //             // )
        //         },
        //         error : function(xhr,errmsg,err) {
        //         console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        //     }
        //     });
        // });

        // $.ajax({
        //     type:"POST",
        //     url:'',
        //     data:{
        //         'csrfmiddlewaretoken': csrf[0].value,
        //         'ratings':val_num,
        //         'description':$('#desc').val()
        //     },
        //     success:function (response){
        //         console.log(response)
        //         confirmbox.innerHTML='rated'
                
        //     },
        //     error:function(error){
        //         console.log(error)
        //         confirmbox.innerHTML='error'
        //     }
           
        // }
        
        // )