// console.log('Hello world')

console.log("hello world")

// get stars

const one=document.getElementById('first')

const two=document.getElementById("second")

const three=document.getElementById("third")

const four=document.getElementById("fourth")

const five=document.getElementById("fifth")

const form= document.querySelector('form')
// const confirmbox = document.getElementById('rate-it')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

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
        console.log(val_num)

        form.addEventListener('submit',e=>{
            e.preventDefault()
            // const id = e.target.id
            console.log('in')

            const val_num = getNumericValue(val)
            const review = document.getElementById('desc-text')
            

            
            
            $.ajax({
                type:"POST",
                url:'',
                data:{
                    'csrfmiddlewaretoken': csrf[0].value,
                    'ratings':val_num,
                    'description':review.value,
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
        