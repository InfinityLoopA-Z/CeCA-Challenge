
import React, { useState } from 'react';


const Form = (props) => {
    const { sendCarPlate } = props;
    const [carPlate, setCarPlate] = useState('');
    const onChangeCarPlate = (e) => {
        setCarPlate(e.target.value);
    }
  return (
      <>
        <form onSubmit={() => sendCarPlate(carPlate)}>
            <label>
                Car Plate:
                <input 
                    type="text" 
                    name="carPlate"
                    value={carPlate}
                    onChange={onChangeCarPlate}
                />
            </label>
            <button type="submit">
                Submit
            </button>
        </form>
      </>
  );
};
export default Form;