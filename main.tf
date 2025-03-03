provider "hyperv" {}

resource "hyperv_vm" "my_vm" {
  name              = "TerraformVM"
  generation        = 2
  memory_mb         = 4096
  processor_count   = 2
  vhd_path          = "C:\\HyperV\\VirtualHardDisks\\MyVM.vhdx"
  switch_name       = "Default Switch"
  automatic_start   = true
  automatic_stop    = "ShutDown"

  # OS Installation (Use your ISO path)
  boot_device       = "DVD"
  iso_path          = "C:\\ISO\\WindowsServer.iso"
}

output "vm_ip" {
  value = hyperv_vm.my_vm.ip_address
}