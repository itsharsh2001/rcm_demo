import { useState } from 'react';
import './App.css';
import * as XLSX from "xlsx";
import { saveAs } from 'file-saver'
import { utils, writeFile } from 'xlsx';

import axios from 'axios';

function App() {
 
  const [card, setCard] = useState(true)
  const [files, setFiles] = useState([]);
  const [ids, setIds] = useState([]);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    const fieldId = event.target.id;

    setFiles((prevFiles) => [...prevFiles, selectedFile]);
    setIds((prevIds) => [...prevIds, fieldId]);
  };

  const handleFormSubmit = async (event) => {
    event.preventDefault();

    
    const data = {};

    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const id = ids[i];
      const jsonData = await convertToJSON(file);
      // console.log(file);
      // Preprocess numeric column with commas
    // const processedData = jsonData.map((row) => {
    //   const processedRow = { ...row };
    //   const numericValue = row['Amount'];
    //   processedRow['Amount'] = typeof numericValue === 'string' ? numericValue.replace(/,/g, '') : numericValue;
    //   return processedRow;
    // });

      
      // data[id] = processedData
      data[id] = JSON.stringify(jsonData);
      console.log(data[id]);
    }

    try {
      // Send a POST request to the Flask API

      console.log(data);
      
      const response = await axios.post('https://itsharsh2001.pythonanywhere.com/', data,{ responseType: 'blob' });
      // console.log(JSON.parse(response.data.data));
      console.log(response.data);
      // const ans = JSON.parse(response.data.data);
      // const workbook = XLSX.utils.book_new();
      // const worksheet = XLSX.utils.json_to_sheet(ans);
      // XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1');

      // // Generate Excel file buffer
      // const excelBuffer = XLSX.write(workbook, { type: 'array', bookType: 'xlsx' });

      // // Convert buffer to Blob
      // const blob = new Blob([excelBuffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });

      // // Save file using FileSaver.js
      // saveAs(blob, 'data.xlsx');


//       const worksheet = utils.json_to_sheet(JSON.parse(response.data.data));
// const workbook = utils.book_new();
// utils.book_append_sheet(workbook, worksheet, 'Sheet 1');

// // Generate the Excel file
// writeFile(workbook, 'data.xlsx');

const blob = new Blob([response.data], { type: 'application/octet-stream' });
    const downloadUrl = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = 'output.xlsx';
    link.click();
      
    } catch (error) {
      console.error("An error occurred while downloading the file", error);
    }
  };

   const convertToCSV = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();

      reader.onload = (event) => {
        const workbook = XLSX.read(event.target.result, { type: "binary" });
        const worksheet = workbook.Sheets[workbook.SheetNames[0]];
        const csv = XLSX.utils.sheet_to_csv(worksheet);

        resolve(csv);
      };

      reader.onerror = (event) => {
        reject(new Error("Failed to read the file"));
      };

      reader.readAsBinaryString(file);
    });
  };

  const convertToJSON = async (file) => {
    // const csv = await convertToCSV(file);
    // const csvData = CSVToArray(csv);
    // const jsonData = convertArrayToJSON(csvData);
    // return jsonData;

    return new Promise((resolve, reject) => {
      const reader = new FileReader();
  
      reader.onload = (event) => {
        const data = new Uint8Array(event.target.result);
        const workbook = XLSX.read(data, { type: 'array' });
        const worksheetName = workbook.SheetNames[0];
        // console.log(worksheetName);
        const worksheet = workbook.Sheets[worksheetName];
        const jsonData = XLSX.utils.sheet_to_json(worksheet, { raw: false });
        // const jsonData = XLSX.utils.sheet_to_csv(worksheet);
        // console.log(jsonData);
        // Preprocess numeric column with commas
        // const processedData = jsonData.map((row) => {
        //   const processedRow = { ...row };
        //   const numericValue = row['Amount'];
        //   processedRow['Amount'] = typeof numericValue === 'string' ? Number(numericValue.replace(/,/g, '')) : numericValue;
        //   return processedRow;
        // });
  
        resolve(jsonData);
      };
  
      reader.onerror = (event) => {
        reject(event.target.error);
      };
  
      reader.readAsArrayBuffer(file);
    });
  };
  
  const CSVToArray = (csv) => {
    const lines = csv.split("\n");
    const result = [];
    const headers = lines[0].split(",");
    
    for (let i = 1; i < lines.length; i++) {
      const obj = {};
      const currentLine = lines[i].split(",");
      
      for (let j = 0; j < headers.length; j++) {
        obj[headers[j]] = currentLine[j];
      }
      
      result.push(obj);
    }
    
    return result;
  };
  
  const convertArrayToJSON = (array) => {
    const jsonData = JSON.stringify(array);
    return jsonData;
  };
  

  return (
    <>
      {card&&<div className='card'>
        <span onClick={(prevState)=>{setCard(!prevState)}}>
          RCM Analysis
        </span>
      </div>}
      {!card&&<div className='card'>
        <form className='form' onSubmit={handleFormSubmit}>
          <div>
            <label>Transactions File</label>
            <input type="file" name="files" accept=".xlsx,.xls" id='Transactions' onChange={handleFileChange} />
          </div>
          <div>
            <label>Keyword Master File</label>
            <input type="file" name="files" accept=".xlsx,.xls" id='KeywordMaster' onChange={handleFileChange} />
          </div>
          <div>
            <label>SAC Master File</label>
            <input type="file" name="files" accept=".xlsx,.xls" id='SACMaster' onChange={handleFileChange} />
          </div>
          <div>
            <label>Client File</label>
            <input type="file" name="files" accept=".xlsx,.xls" id='ClientDetails' onChange={handleFileChange} />
          </div>
          <div>
            <label>Vendor_List File</label>
            <input type="file" name="files" accept=".xlsx,.xls" id='VendorDetails' onChange={handleFileChange} />
          </div>
          <div>
            <label>Directors File</label>
            <input type="file" name="files" accept=".xlsx,.xls" id='Directors' onChange={ handleFileChange} />
          </div>
          <div>
            <label>Testing File</label>
            <input type="file" name="files" accept=".xlsx,.xls" id='Testing' onChange={ handleFileChange} />
          </div>
          {/* Add more file input fields as needed */}
          <button type="submit">Process Files</button>
        </form>
        {/* <button onClick={handleDownload}>Download Excel</button> */}
      </div>}
    </>
  );
}

export default App;
