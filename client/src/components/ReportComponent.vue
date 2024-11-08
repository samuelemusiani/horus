<template>
    <div class="grid grid-cols-2 items-center justify-center w-4/5 mx-auto">
        <h3 class="mx-auto my-8 text-xl font-bold text-gray-700">Device Analysis</h3>
        <h3 class="mx-auto my-8 text-xl font-bold text-gray-700">Service Analysis</h3>
        <div> 
            <Doughnut :data="chartDataDevices" :options="chartOptions" />
        </div>
        <div>
            <Doughnut :data="chartDataServices" :options="chartOptions" />
        </div>
    </div>
</template>

<script>
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Doughnut } from 'vue-chartjs';
ChartJS.register(ArcElement, Tooltip, Legend);

export default {
    name: 'ReportComponent',
    components: {
        Doughnut
    },
    props: {
        devices: {
            type: Array,
            required: true,
        }
    },
    computed: {
        vulnerableDeviceCount() {
            return this.devices.filter(device => device.services.some(service => service.ifVulnerable)).length;
        },
        vulnerableServiceCount() {
            let services = this.devices.map(device => device.services);
            services = services.flat();
            return services.filter(service => service.ifVulnerable).length;
        },
        chartDataDevices() {
            return {
                labels: ['Safe devices', 'Vulnerable devices'],
                datasets: [
                    {
                        backgroundColor: ['#41B883', '#DD1B16'],
                        data: [this.devices.length - this.vulnerableDeviceCount, this.vulnerableDeviceCount]
                    }
                ]
            };
        },
        chartDataServices(){
            let services = this.devices.map(device => device.services);
            services = services.flat();
            return {
                labels: ['Safe services', 'Vulnerable services'],
                datasets: [
                    {
                        backgroundColor: ['#41B883', '#DD1B16'],
                        data: [services.length - this.vulnerableServiceCount, this.vulnerableServiceCount]
                    }
                ]
            };
        },
        chartOptions() {
            return {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                },
            };
        }
    }
};
</script>

<style></style>