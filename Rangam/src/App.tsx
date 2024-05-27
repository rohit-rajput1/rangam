import { useEffect, useState } from 'react'
import axios from 'axios'
import './App.css'

function App() {
    const cars = [
        {name: 'Tesla Model S', color: 'red', photoUrl: 'https://cdni.autocarindia.com/Utils/ImageResizer.ashx?n=https://cdni.autocarindia.com/ExtraImages/20240229122047_Tesla_Roadster.jpg&w=700&c=1'},
        {name: 'BMW M3', color: 'gray', photoUrl: 'https://www.topgear.com/sites/default/files/2022/09/1-BMW-3-Series.jpg?w=976&h=549'},
        {name: 'Audi R8', color: 'blue', photoUrl: 'https://www.topgear.com/sites/default/files/2023/09/33136-RS7PERFORMANCEASCARIBLUEJORDANBUTTERS208.jpg?w=976&h=549'},
    ]
    useEffect(() => {
      const applesListUrl = 'http://localhost:8000/'
      axios.get<Apple[]>(applesListUrl)
          .then(response => setApples(response.data))
  }, [])
    return (
        <>
            <div className="flex-container">
                {cars.map((car, index) => (
                    <div className="bg-white rounded-lg shadow-md overflow-hidden card" key={index}>
                        <img
                            src={car.photoUrl}
                            alt={`The ${car.name} car, which comes in a stunning ${car.color} color.`}
                            className="w-full h-48 object-cover"
                            width="400"
                            height="300"
                        />
                        <div className="p-4">
                            <h3 className="text-lg font-semibold text-gray-800 mb-2">{car.name}</h3>
                            <p className="text-gray-600">Color: {car.color}</p>
                        </div>
                    </div>
                ))}
            </div>
        </>
    )
}

export default App
