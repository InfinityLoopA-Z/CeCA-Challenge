const Form = (props) => {
    const { sendCarPlate, car, setCar } = props;
    
    const onChangeCarPlate = (e) => {
        e.preventDefault();
        setCar(e.target.value);
    }

    return (
        <>
            <div>
                <label>
                    Car Plate:
                    <input 
                        type="text" 
                        name="carPlate"
                        value={car}
                        onChange={onChangeCarPlate}
                    />
                </label>
                <button onClick={() => sendCarPlate(car)}>
                    Submit
                </button>
            </div>
        </>
    );
};
export default Form;