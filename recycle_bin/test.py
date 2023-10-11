from recycle_bin.recycle_one.models import Material

def materials_filter():
    #crea una lista con los materiales aptos para reciclaje
    selectable_materials = Material.objects.all()
    print (selectable_materials)


materials_filter()