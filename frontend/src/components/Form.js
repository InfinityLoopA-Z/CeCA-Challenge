const Form = (props) => {
    const { sendCarPlate, car, setCar } = props;
    
    const onChangeCarPlate = (e) => {
        e.preventDefault();
        setCar(e.target.value);
    }

    return (
        <>
            <form>
                <label>
                    Car Plate:
                    <input 
                        type="text" 
                        name="carPlate"
                        value={car}
                        onChange={onChangeCarPlate}
                    />
                </label>
                <button type="submit" onClick={() => sendCarPlate(car)}>
                    Submit
                </button>
            </form>
        </>
    );
};
export default Form;