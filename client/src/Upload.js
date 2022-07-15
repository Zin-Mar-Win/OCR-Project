import React, { Component } from "react";
import FileBase64 from "./react-file-base64";
import { Button, Form, FormGroup, Label, FormText, Input } from "reactstrap";

import "./upload.css";

class Upload extends Component {
  constructor(props) {
    super(props);

    this.state = {
      confirmation: "",
      isLoading: "",
      files: "",
      Invoice: "",
      Amount: "",
      InvoiceDate: "",
      Vendor: "",
      Description: "",
      CustomerName: "",
    };

    this.handleChane = this.handleChane.bind(this);
  }

  handleChane(event) {
    event.preventDefault();
    const target = event.target;
    const value = target.value;
    //const name = target.name;

    this.setState({ name: value });
  }

  async handleSubmit(event) {
    event.preventDefaulr();
    this.setState({ confirmation: "Uploading..." });
  }

  async getFiles(files) {
    this.setState({
      isLoading: "Extracting data",
      files: files,
    });
    console.log("Base64", this.state.files[0].base64);
    //const UID = Math.round(1 + Math.random() * (1000000 - 1));

    var date = {
      // fileExt: "png",
      // imageID: UID,
      // folder: UID,

      uri: this.state.files[0].uri,
      //name: this.state.files[0].name,
      type: this.state.files[0].type,
      base64: this.state.files[0].base64,
    };

    this.setState({ confirmation: "Processing..." });
    this.setState({ CustomerName: "" });
    this.setState({ InvoiceDate: "" });
    this.setState({ Invoice: "" });
    this.setState({ Amount: "" });
    fetch(
      "/ocrProcessing",

      {
        method: "POST",
        headers: {
          //Accept: "application/json",
          "Content-Type": "multipart/form-data",
          //uploadType: FileBase64,
        },
        body: JSON.stringify(date),
      }
    )
      .then((res) => res.json())
      .then((data) => {
        this.setState({ CustomerName: "" });
        this.setState({ InvoiceDate: "" });
        this.setState({ Invoice: "" });
        this.setState({ Amount: "" });
        //console.log(data.body);
        data.NAME.map((name, i) => {
          this.setState({ CustomerName: this.state.CustomerName + " " + name });
        });
        data.DATE.map((dat, i) => {
          this.setState({ InvoiceDate: this.state.InvoiceDate + " " + dat });
        });
        data.NUMBER.map((num, i) => {
          this.setState({ Invoice: this.state.Invoice + " " + num });
        });
        data.TOTAL.map((amount, i) => {
          this.setState({ Amount: this.state.Amount + " " + amount });
        });

        //data.body.map((field, index) => {
        //console.log(index, " ", field);
        // this.setState({ Amount: data.body[0] + "" });
        // this.setState({ Invoice: data.body[1] + "" });
        // this.setState({ InvoiceDate: data.body[2] + "" });
        // this.setState({ CustomerName: data.body[3] + "" });
        // this.setState({ Description: data.body[4] + "" });
        // });
      });
    console.log("data is ", this.state.data);

    //'https://31gv9av7oe.execute-api.us-west-1.amazonaws.com/Production',
    // await fetch(
    //   " https://odnqtpy2ei.execute-api.ap-southeast-1.amazonaws.com/Production/",
    //   {
    //     method: "POST",
    //     headers: {
    //       Accept: "application/json",
    //       "Content-Type": "application.json",
    //     },
    //     body: JSON.stringify(date),
    //   }
    // );

    // let targetImage = UID + ".png";
    // //
    // //async function fetchMovies() {
    // //const response =
    // fetch(
    //   " https://odnqtpy2ei.execute-api.ap-southeast-1.amazonaws.com/Production/ocr-test",

    //   {
    //     method: "POST",
    //     headers: {
    //       Accept: "application/json",
    //       "Content-Type": "application.json",
    //     },
    //     body: JSON.stringify(targetImage),
    //   }
    // )
    //   .then((res) => res.json())
    //   .then((data) => {
    //     console.log(data.body);
    //     //data.body.map((field, index) => {
    //     //console.log(index, " ", field);
    //     this.setState({ Amount: data.body[0] + "" });
    //     this.setState({ Invoice: data.body[1] + "" });
    //     this.setState({ InvoiceDate: data.body[2] + "" });
    //     this.setState({ CustomerName: data.body[3] + "" });
    //     this.setState({ Description: data.body[4] + "" });
    //     // });
    //   });
    //console.log(response.json());
    //const OCRBody = await response.json();
    //console.log("OCRBody", OCRBody);

    // this.setState({ Amount: response.json().body[0] });
    // this.setState({ Invoice: response.json().body[1] });
    // this.setState({ InvoiceDate: response.json().body[2] });
    //return response.json();
    //}
    //fetchMovies();

    // this.setState({ confirmation: "" });

    //
  }

  render() {
    const processing = this.state.confirmation;
    return (
      <div className="row">
        <div className="col-6 offset-3">
          <Form onSubmit={this.handleSubmit}>
            <FormGroup>
              <h3 className="text-danger">{processing}</h3>
              <h6>Upload Invoice</h6>
              <FormText color="muted">PNG,JPG</FormText>

              <div className="form-group files color">
                <FileBase64
                  multiple={true}
                  onDone={this.getFiles.bind(this)}
                ></FileBase64>
              </div>
            </FormGroup>
            <FormGroup>
              <Label>
                <h6>Invoice</h6>
              </Label>
              <img
                src={this.state.files !== "" ? this.state.files[0].base64 : ""}
                alt="Red dot"
              />
            </FormGroup>
            <FormGroup>
              <Label>
                <h6>Invoice</h6>
              </Label>
              <Input
                type="text"
                name="Invoice"
                id="Invoice"
                required
                value={this.state.Invoice}
                onChange={this.handleChane}
              />
            </FormGroup>

            <FormGroup>
              <Label>
                <h6>Amount ($)</h6>
              </Label>
              <Input
                type="text"
                name="Amount"
                id="Amount"
                required
                value={this.state.Amount}
                onChange={this.handleChane}
              />
            </FormGroup>

            <FormGroup>
              <Label>
                <h6>Date</h6>
              </Label>
              <Input
                type="text"
                name="InvoiceDate"
                id="InvoiceDate"
                required
                value={this.state.InvoiceDate}
                onChange={this.handleChane}
              />
            </FormGroup>

            <FormGroup>
              <Label>
                <h6>Vendor</h6>
              </Label>
              <Input
                type="text"
                name="Vendor"
                id="Vendor"
                required
                value={this.state.CustomerName}
                onChange={this.handleChane}
              />
            </FormGroup>

            <FormGroup>
              <Label>
                <h6>Description</h6>
              </Label>
              <Input
                type="text"
                name="Description"
                id="Description"
                required
                value={this.state.Description}
                onChange={this.handleChane}
              />
            </FormGroup>
            <Button className="btn btn-lg btn-block  btn-success">
              Submit
            </Button>
          </Form>
        </div>
      </div>
    );
  }
}

export default Upload;
