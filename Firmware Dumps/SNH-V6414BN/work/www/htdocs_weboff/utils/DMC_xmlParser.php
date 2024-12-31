<?php
class XMLParser 
{
    private $parser;
    private $xml;
    public $document;
    private $stack;
    private $cleanTagNames;
    
    function __construct($xml = '', $cleanTagNames = true)
    {
        $this->xml = $xml;
        $this->stack = array();
        $this->cleanTagNames = $cleanTagNames;
    }
    public function Parse()
    {
        $this->parser = xml_parser_create();
        xml_set_object($this->parser, $this);
        xml_set_element_handler($this->parser, 'StartElement', 'EndElement');
        xml_set_character_data_handler($this->parser, 'CharacterData');

        if (!xml_parse($this->parser, $this->xml))
            $this->HandleError(xml_get_error_code($this->parser), xml_get_current_line_number($this->parser), xml_get_current_column_number($this->parser));
        xml_parser_free($this->parser);
    }
    
    private function HandleError($code, $line, $col)
    {
        trigger_error('XML Parsing Error at '.$line.':'.$col.'. Error '.$code.': '.xml_error_string($code));
    }

    public function GenerateXML()
    {
        return $this->document->GetXML();
    }

    private function GetStackLocation()
    {
        return end($this->stack);
    }

    private function StartElement($parser, $name, $attrs = array())
    {
        $name = strtolower($name);
        if (count($this->stack) == 0) 
        {
            $this->document = new XMLTag($name, $attrs);
            $this->stack = array(&$this->document);
        }
        else
        {
            $parent = $this->GetStackLocation();
            $parent->AddChild($name, $attrs, count($this->stack), $this->cleanTagNames);
            if($this->cleanTagNames)
                $name = str_replace(array(':', '-'), '_', $name);
            $this->stack[] = end($parent->$name);        
        }
    }

    private function EndElement($parser, $name)
    {
        array_pop($this->stack);
    }

    private function CharacterData($parser, $data)
    {
        $tag = $this->GetStackLocation();
        $tag->tagData .= $data;
    }
}

class XMLTag
{
    public $tagAttrs;
    public $tagName;
    public $tagData;
    public $tagChildren;
    public $tagParents;

    function __construct($name, $attrs = array(), $parents = 0)
    {
        $this->tagAttrs = array_change_key_case($attrs, CASE_LOWER);
        $this->tagName = strtolower($name);
        $this->tagParents = $parents;
        $this->tagChildren = array();
        $this->tagData = '';
    }
    
    public function AddChild($name, $attrs, $parents, $cleanTagName = true)
    {    
        if(in_array($name, array('tagChildren', 'tagAttrs', 'tagParents', 'tagData', 'tagName')))
        {
            trigger_error('You have used a reserved name as the name of an XML tag.', E_USER_ERROR);
            return;
        }

        $child = new XMLTag($name, $attrs, $parents);
        if($cleanTagName)
            $name = str_replace(array(':', '-'), '_', $name);
        elseif(strstr($name, ':') || strstr($name, '-'))
            trigger_error('Your tag named "'.$name.'" contains either a dash or a colon.', E_USER_NOTICE);
        if(!isset($this->$name))
            $this->$name = array();
        $this->{$name}[] = &$child;
        $this->tagChildren[] = &$child;
        return $this;
    }

    public function GetXML()
    {
        $out = "\n".str_repeat("\t", $this->tagParents).'<'.$this->tagName;
        foreach($this->tagAttrs as $attr => $value)
            $out .= ' '.$attr.'="'.$value.'"';
        if(empty($this->tagChildren) && empty($this->tagData))
            $out .= " />";
        else
        {    
            if(!empty($this->tagChildren))
            {
                $out .= '>';
                foreach($this->tagChildren as $child)
                    $out .= $child->GetXML();
                $out .= "\n".str_repeat("\t", $this->tagParents);
            }
            elseif(!empty($this->tagData))
                $out .= '>'.$this->tagData;
            $out .= '</'.$this->tagName.'>';
        }
        
        return $out;
    }

    public function Delete($childName, $childIndex = 0)
    {
        $this->{$childName}[$childIndex]->DeleteChildren();

        $this->{$childName}[$childIndex] = null;

        unset($this->{$childName}[$childIndex]);

        for($x = 0; $x < count($this->tagChildren); $x ++)
        {
            if(is_null($this->tagChildren[$x]))
                unset($this->tagChildren[$x]);
        }
    }
    
    private function DeleteChildren()
    {
        for($x = 0; $x < count($this->tagChildren); $x ++)
        {
            $this->tagChildren[$x]->DeleteChildren();
            $this->tagChildren[$x] = null;
            unset($this->tagChildren[$x]);
        }
    }
}
?>
