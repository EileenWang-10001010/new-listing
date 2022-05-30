import React, { useState } from 'react';
import internal from 'stream';

const server = process.env.API_URL || 'http://127.0.0.1:9000';

type formType = {
  name: string,
  category: string,
  price: string,
  discount: string,
  image:  File | string,
}

export const Listing: React.FC<{}> = () => {
  const initialState = {
    name: "",
    category: "",
    price: "",
    discount: "",
    image: "",
  };
  
  const [values, setValues] = useState<formType>(initialState);

  const onChange = (event: React.ChangeEvent<HTMLInputElement>) => {
      setValues({ ...values, [event.target.name]: event.target.value });
  };
  const onFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setValues({ ...values, [event.target.name]: event.target.files![0] });
  };

  const onSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
   
    const data = new FormData()
    data.append('name', values.name)
    data.append('category', values.category)
    data.append('price',values.price)
    data.append('discount',values.discount)
    data.append('image', values.image)

    fetch(server.concat('/items'), {
      method: 'POST',
      mode: 'cors',
      body: data,
    })
    .then(response => response.json())
    .then(data => {
      console.log('POST success:', data);
      setValues(initialState);
    })
    .catch((error) => {
      console.error('POST error:', error);
    })
  };
  return (
    <div className='Listing'>
      <form onSubmit={onSubmit}>
        <div>
            <input type='text' name='name' id='name' placeholder='name' onChange={onChange} required/>
            <input type='text' name='category' id='category' placeholder='category' onChange={onChange}/>
            <input type='text' name='price' id='price' placeholder='price' onChange={onChange}/><span>¥ </span>
            <input type='text' name='discount' id='discount' placeholder='discount % off' onChange={onChange}/><span>% off </span>
            <input type='file' name='image' id='image' placeholder='image' onChange={onFileChange}/>
            <button type='submit'>List this item</button>
        </div>
      </form>
    </div>

  );
}