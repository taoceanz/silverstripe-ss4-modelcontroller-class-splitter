<?php

use SilverStripe\Dev\BuildTask;
use SilverStripe\Control\Director;
use SilverStripe\Security\Permission;
use SilverStripe\Security\Security;

/**
 * Task to split SS3 Model and Controller classes into their own files
 */
class ModelControllerClassSplitter extends BuildTask
{
    protected $title = "Model/Controller class splitter";

    protected $description = "Split SS3 model and controller classes in the same file into their own files.";

    /**
     * Ensure sufficient permission
     *
     * @return void
     */
    public function init()
    {
        parent::init();

        $canAccess
            = Director::isDev()
            || Director::is_cli()
            || Permission::check("ADMIN");

        if (!$canAccess) {
            return Security::permissionFailure($this);
        }
    }

    /**
     * Run task to split model and controller classes into their own files
     *
     * @param [type] $request
     * 
     * @return void
     */
    public function run($request)
    {
        echo "Splitting classes.";
    }
}