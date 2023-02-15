import bpy
from bpy.types import Panel
from bpy.types import Operator

bl_info = {
        "name": "Realize Instances",
        "description": "Make instance real from Geo nodes and replace with selected object.",
        "author": "7Bajwa",
        "version": (0, 0, 1),
        "blender": (3, 3, 0),
        "location": "View3D",
        "category": "Generic"
        }


class RealizeInstancesPanel(Panel):
    """Panel for creating instances of selected objects and replacing them with a selected object"""
    bl_label = "Realize Instances"
    bl_idname = "OBJECT_PT_realize_instances"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout
        layout.prop_search(context.scene, "replace_object", bpy.data, "objects", text="Replace Object")
        layout.operator(AddInstancesToCollection.bl_idname)
        


class AddInstancesToCollection(Operator):
    """Add instances of selected objects to a collection and replace them with the selected object"""
    bl_idname = "object.add_instances_to_collection"
    bl_label = "Realize Instances"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        selected_objects = bpy.context.selected_objects

        for obj in selected_objects:
            
            bpy.ops.object.duplicates_make_real(use_base_parent=False, use_hierarchy=False)
            bpy.ops.object.move_to_collection(collection_index=0, is_new=True, new_collection_name=obj.name)
            col = bpy.data.collections.get(obj.name)
            
            for ob in col.objects:
                ob.modifiers.clear()
                ob.data = bpy.data.objects[context.scene.replace_object].data
               
        return {'FINISHED'}




def register():
    bpy.utils.register_class(RealizeInstancesPanel)
    bpy.types.Scene.replace_object = bpy.props.StringProperty(
        name="Replace Object",
        description="Object to replace instances with",
        default=""
    )
    bpy.utils.register_class(AddInstancesToCollection)
   

def unregister():
    bpy.utils.unregister_class(RealizeInstancesPanel)
    del bpy.types.Scene.replace_object
    bpy.utils.unregister_class(AddInstancesToCollection)
   

if __name__ == '__main__':
    register()