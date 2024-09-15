<template>
    <NavBar></NavBar>
    <div class="container-fluid" style="width: 1000px; margin-top: 1px;">
            <div class="col-2 col-sm-4 col-md-6 col-lg-12">
                <div class="input-group mb-4">
                    <input type="text" class="form-control" v-model="flightNumber" placeholder="Flight Number" aria-label="Flight Number" aria-describedby="button-addon2" style="width: 90%">
                    <button class="btn btn-primary" type="button" @click="displayFlight" :disabled="isFlightNumberEmpty">Search</button>
                </div>
            
        </div>
    
        <div class="container border rounded-pill p-5 d-flex justify-content-center" v-if="outputButtonVisible">
            <button type="button" class="button border border-2 outputFlight btn btn-light fs-3 d-flex justify-content-between align-items-center" style="width: 80%" data-bs-toggle="modal" data-bs-target="#flightdetails">
                <span class="text-start ms-5 me-auto">Flight {{ flightNumber }}</span>
                <img src="../assets/94999.png" class="img" style="width: 300px;">
            </button>
            </div>

    <!-- Popup Modal -->
    <div class="modal fade modal-xl" id="flightdetails"  tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">Flight Details</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <h3><strong>Flight {{ flightNumber }}</strong></h3>
                    <h4>Status:</h4><h4 class="text-danger">Cancelled</h4>
                    <h4>Departure Time: 9.00 a.m.</h4>
                    <h4>Arrival Time: 10.00 a.m.</h4>

                    <h3>Passenger List</h3>
                    <div class="border "></div>
                    <br>
                    <div class="btn-group-toggle" data-toggle="buttons">
                        <label class="btn btn-outline-primary p-2">
                            <input type="checkbox" autocomplete="off"> John Lim
                        </label> <br> 
                        <label class="btn btn-outline-primary p-2">
                            <input type="checkbox" autocomplete="off"> Tim Tam
                        </label> <br>
                        <label class="btn btn-outline-primary p-2">
                            <input type="checkbox" autocomplete="off"> Tam Tim
                        </label> <br>
                        <label class="btn btn-outline-primary p-2">
                            <input type="checkbox" autocomplete="off"> Joe Mama
                        </label> <br>
                    </div>

                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#flightrebooking" >Make Booking</button>
                </div>
            </div>
        </div>
    </div>
    <div class="modal fade modal-xl" id="flightrebooking"  tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">Choose Flight to Rebook</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="btn-group-toggle" data-toggle="buttons">
                        <label class="btn btn-outline-primary">
                            <input type="checkbox" autocomplete="off"> <h3>Flight 1112</h3>
                                <p>Destination: San Juan<br> 
                                    Departure Date: 5 April 2024<br>
                                    Departure Time: 2pm<br>
                                </p>
                                
                        </label> <br> 
                        <label class="btn btn-outline-primary">
                            <input type="checkbox" autocomplete="off"> <h3>Flight 1234</h3>
                                <p>Destination: San Andreas<br> 
                                    Departure Date: 6 April 2024<br>
                                    Departure Time: 4pm<br>
                                </p>
                        </label> <br>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#bookingsuccess" >Confirm Booking</button>
                </div>
            </div>
        </div>
    </div>
    <div class="modal fade modal-xl" id="bookingsuccess"  tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">Booking Successful!</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    
                    <h3>Booking has been created!</h3>
                        <p>Please alert the customer of the newly created booking!
                        </p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>
    
  </div>
</template>
<script setup>
import NavBar from './NavBar.vue';
</script>

<script scoped>


export default {
    name: 'PassengerManagement',
    data() {
    return {
      flightNumber: '',
      outputButtonVisible: false
    }
  },
  watch: {
    flightNumber() {
      this.outputButtonVisible = false;
    }
  },
  computed: {
    isFlightNumberEmpty() {
      return this.flightNumber.trim() === '';
    }
  },
  
  methods: {
    displayFlight() {
      this.outputButtonVisible = true;
    },
    
    
  }
}
</script>

<style scoped>
.btn-group-toggle .btn {
  width: 90%;
  text-align: left;
}
.full-screen-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    width: 70vw;
    /* background-color: #f9f9f9; */
}
.button {
  width: 80px;
  height: 90px;
  padding: 0;
  
}

.img {
  width: 50%;
  height: 100%;
  overflow: hidden;
}
</style>

